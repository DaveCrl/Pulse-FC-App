import os
import re
import json
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright, Page, Locator, TimeoutError as PlaywrightTimeoutError

# ==========================================
# 0. CONFIGURATION & LOGS
# ==========================================

BASE_URL = "https://www.ea.com/fr/games/ea-sports-fc/ratings"

# Setup Paths for Web App Integration
# We generate directly inside the module's "public" folder (ready for Vite/Next.js)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")

ASSETS_DIR = os.path.join(PUBLIC_DIR, "assets", "playstyles")
ASSETS_PLUS_DIR = os.path.join(PUBLIC_DIR, "assets", "playstyles_plus")
DATA_DIR = os.path.join(PUBLIC_DIR, "data")
JSON_FILE = os.path.join(DATA_DIR, "ea_playstyles.json")

# Frontend Relative Paths
FRONTEND_ASSETS_PATH = "/assets/playstyles"
FRONTEND_ASSETS_PLUS_PATH = "/assets/playstyles_plus"
FALLBACK_ICON_PATH = "/assets/playstyles/fallback-placeholder.png"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"
})


# ==========================================
# UTILITAIRES
# ==========================================

def setup_directories() -> None:
    """Prepares the required Vite / React static directories."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    os.makedirs(ASSETS_PLUS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)


def slugify(text: str) -> str:
    """Convert a standard string into a stable slug."""
    text = text.strip().lower()
    text = text.replace("+", "") # Strip the '+' character completely to link normal/plus
    replacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a", "ä": "a",
        "î": "i", "ï": "i",
        "ô": "o", "ö": "o",
        "ù": "u", "û": "u", "ü": "u",
        "ç": "c", "œ": "oe",
        "’": "'", "“": '"', "”": '"'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text


def clean_drop_assets_url(url: str) -> str:
    """Format the EA drop assets URL to get a higher quality image."""
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return f"{base}?im=Resize=(2560)&q=80"


def guess_extension(file_url: str) -> str:
    """Guess the file extension from the raw URL."""
    path = urlparse(file_url).path.lower()
    _, ext = os.path.splitext(path)
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]:
        return ext
    return ".png"


def download_file(url: str, filepath: str) -> bool:
    """Download an asset; returns False if it fails (triggers fallback)."""
    if not url:
        return False
    try:
        r = session.get(url, timeout=20)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        return True
    except requests.RequestException as e:
        logging.warning(f"Download failed for {url} -> {e}")
        return False


def scroll_to_bottom(page: Page) -> None:
    """Smoothly script scroll to guarantee element rendering."""
    page.evaluate("""
        async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                let distance = 300;
                let timer = setInterval(() => {
                    let scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if(totalHeight >= scrollHeight - window.innerHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        }
    """)
    page.wait_for_timeout(1000)
    page.mouse.wheel(0, -600)
    page.wait_for_timeout(500)


def safe_click_tab(page: Page, text_value: str, timeout: int = 3000) -> bool:
    """Safely find and click a category tab."""
    candidates = [
        f'button[aria-label="{text_value}"]',
        f'button:has-text("{text_value}")',
        f'div[role="tab"]:has-text("{text_value}")',
        f'span:has-text("{text_value}")',
        f'a:has-text("{text_value}")'
    ]
    for selector in candidates:
        try:
            locator = page.locator(selector)
            if locator.count() > 0 and locator.first.is_visible():
                locator.first.click(timeout=timeout)
                page.wait_for_timeout(1200)
                return True
        except PlaywrightTimeoutError:
            continue
        except Exception:
            continue
    return False


def pick_best_drop_asset_from_card(card: Locator) -> Optional[str]:
    """Find the best quality image URL from a card element."""
    imgs = card.locator("img")
    for i in range(imgs.count()):
        src = imgs.nth(i).get_attribute("src")
        if src and "drop-assets.ea.com" in src:
            return clean_drop_assets_url(src)

    sources = card.locator("source")
    best, best_score = None, -1

    for i in range(sources.count()):
        srcset = sources.nth(i).get_attribute("srcset")
        if not srcset: continue

        for candidate in [part.strip().split(" ")[0] for part in srcset.split(",")]:
            if "drop-assets.ea.com" not in candidate: continue
            score = 0
            m = re.search(r"Resize=\((\d+)\)", candidate)
            if m: score = int(m.group(1))
            
            if score > best_score:
                best_score = score
                best = candidate

    return clean_drop_assets_url(best) if best else None


# ==========================================
# 1. PHASE DE SCRAPING (EXTRACTION)
# ==========================================

def extract_cards(page: Page, category: str, is_plus: bool) -> List[Dict[str, Any]]:
    """Extract individual cards appearing on screen bounds."""
    results = []
    seen = set()

    cards = page.locator('a[href*="/ratings/abilities-ratings/"]')
    for i in range(cards.count()):
        card = cards.nth(i)
        href = card.get_attribute("href")
        if not href: continue

        full_url = f"https://www.ea.com{href}" if href.startswith("/") else href
        if is_plus and "/play-style-plus/" not in full_url: continue
        if (not is_plus) and "/play-style/" not in full_url: continue

        if full_url in seen: continue
        seen.add(full_url)

        label = card.inner_text().strip().replace("\n", " ").strip()
        label = re.sub(r"\s+", " ", label)
        if not label: continue

        icon_url = pick_best_drop_asset_from_card(card)
        
        results.append({
            "label": label,
            "page_url": full_url,
            "icon_url": icon_url, # None represents a missing icon from the DOM
            "is_plus": is_plus,
            "category": category
        })

    return results


def collect_mode(page: Page, mode_text: str, is_plus: bool) -> List[Dict[str, Any]]:
    """Switch primary modes and cycle categories."""
    collected = []
    
    if safe_click_tab(page, mode_text):
        logging.info(f"✔ Mode activated: {mode_text}")
    else:
        logging.warning(f"⚠ Mode {mode_text} click failed.")

    # Primary pass (Base layout values)
    scroll_to_bottom(page)
    collected.extend(extract_cards(page, category="Général", is_plus=is_plus))

    # Category Tab Pass
    categories = ["Buts", "Contrôle du ballon", "Défensifs", "Finition", "Gardien", "Passe", "Physique"]
    for cat in categories:
        if safe_click_tab(page, cat):
            logging.info(f"   -> Scraping tab: {cat}")
            scroll_to_bottom(page)
            collected.extend(extract_cards(page, category=cat, is_plus=is_plus))

    # Priority deduplication (specific category wins over 'Général')
    dedup = {}
    for item in collected:
        url = item["page_url"]
        if url not in dedup or dedup[url]["category"] == "Général":
            dedup[url] = item

    return list(dedup.values())


def run_scraping() -> List[Dict[str, Any]]:
    """Initializes Playwright and strictly runs the extraction phase."""
    setup_directories()
    all_raw_data = []

    with sync_playwright() as p:
        logging.info("Starting Headless Browser Instance...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1080})

        try:
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector('a[href*="/ratings/abilities-ratings/"]', state="visible", timeout=30000)
            logging.info("EA Ratings fully loaded.")
        except PlaywrightTimeoutError:
            logging.error("Fatal Timeout waiting for EA Web Page DOM.")
            browser.close()
            return []

        # PlayStyles Plus
        logging.info("\n--- Phase 1: PlayStyles+ Extraction ---")
        plus_items = collect_mode(page, "Play Style Plus", is_plus=True)
        all_raw_data.extend(plus_items)

        # Standard PlayStyles
        logging.info("\n--- Phase 2: Standard PlayStyles Extraction ---")
        base_items = collect_mode(page, "Play Style", is_plus=False)
        all_raw_data.extend(base_items)

        browser.close()

    logging.info(f"Extracted {len(all_raw_data)} total unrefined PlayStyles.")
    return all_raw_data


# ==========================================
# 2. PHASE DE TRANSFORMATION
# ==========================================

def transform_and_download(raw_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Downloads assets, handles fallbacks, and standardizes payload for Application."""
    logging.info("\n--- Phase 3: Data Transformation & Assets Downloading ---")
    
    transformed_data = {
        "playstyles": [],
        "playstyles_plus": []
    }

    for item in raw_items:
        label = item["label"]
        raw_icon = item["icon_url"]
        slug = slugify(label)
        
        # Decide exact target based on whether it is "Plus"
        is_plus = item["is_plus"]
        local_dir = ASSETS_PLUS_DIR if is_plus else ASSETS_DIR
        frontend_base = FRONTEND_ASSETS_PLUS_PATH if is_plus else FRONTEND_ASSETS_PATH
        
        # Setup Filepaths
        ext = guess_extension(raw_icon) if raw_icon else ".png"
        filename = f"{slug}{ext}"
        filepath_full = os.path.join(local_dir, filename)

        # Fallback mechanism
        fallback_used = False
        if raw_icon:
            success = download_file(raw_icon, filepath_full)
            if not success:
                fallback_used = True
        else:
            fallback_used = True
            
        final_frontend_path = FALLBACK_ICON_PATH if fallback_used else f"{frontend_base}/{filename}"

        if fallback_used:
            logging.warning(f"⚠ Missing/Failed Image -> {label} (Using Fallback)")
        else:
            logging.info(f"✔ Downloaded -> {label} [{item['category']}]")

        # Frontend JSON Mapping
        out_item = {
            "slug": slug,
            "label_fr": label,
            "category": item["category"],
            "is_plus": is_plus,
            "icon": final_frontend_path
        }

        # Segregation
        if is_plus:
            transformed_data["playstyles_plus"].append(out_item)
        else:
            transformed_data["playstyles"].append(out_item)
            
        time.sleep(0.1)

    return transformed_data


# ==========================================
# 3. PHASE D'EXPORT
# ==========================================

def export_json(final_data: Dict[str, List[Dict[str, Any]]]) -> None:
    """Exports structured data sequentially."""
    logging.info(f"\n--- Phase 4: Final JSON Export ---")
    
    count_base = len(final_data["playstyles"])
    count_plus = len(final_data["playstyles_plus"])
    
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    logging.info("✅ Generation fully completed.")
    logging.info(f"📊 PlayStyles Saved: {count_base}")
    logging.info(f"📊 PlayStyles+ Saved: {count_plus}")
    logging.info(f"📁 JSON File saved at: {JSON_FILE}")


# ==========================================
# POINT D'ENTRÉE PRINCIPAL
# ==========================================

def main() -> None:
    logging.info("Starting EA PlayStyles Scraper module initialization...")
    
    # 1. Scraping
    raw_data = run_scraping()
    if not raw_data:
        logging.error("No raw data collected. Exiting pipeline.")
        return
        
    # 2. Transformation
    app_data = transform_and_download(raw_data)
    
    # 3. Export
    export_json(app_data)


if __name__ == "__main__":
    main()
