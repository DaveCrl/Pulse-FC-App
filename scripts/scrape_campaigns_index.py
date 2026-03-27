import os
import re
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

from playwright.sync_api import sync_playwright, Page, TimeoutError

# ==========================================
# CONFIGURATION
# ==========================================
BASE_URL = "https://www.futbin.com/squads"

# Setup Paths: Scripts is conventionally at the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUT_JSON = os.path.join(DATA_DIR, "campaigns_index.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

# ==========================================
# UTILITAIRES
# ==========================================
def slugify(text: str) -> str:
    """Création d'un slug propre pour l'index."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text

def setup_directories():
    os.makedirs(DATA_DIR, exist_ok=True)

# ==========================================
# SCRAPING LOGIC
# ==========================================
def extract_campaigns(page: Page) -> List[Dict[str, Any]]:
    campaigns = []
    seen = set()
    
    # 🎯 Ajustement du Sélecteur : 
    # Sur l'édition actuelle de FUTBIN, les campagnes principales utilisent la classe "squad-box"
    links = page.locator('a.squad-box')
    
    count = links.count()
    logging.info(f"Found {count} potential squad links on the page.")
    
    for i in range(count):
        el = links.nth(i)
        href = el.get_attribute("href")
        if not href:
            continue
            
        full_url = f"https://www.futbin.com{href}" if href.startswith("/") else href
        
        # Extraction précise du Titre (évite de récupérer "View all X players", "Created:...", etc)
        header_loc = el.locator('.squads-header').first
        if header_loc.count() > 0:
            name = header_loc.inner_text().strip()
        else:
            name = el.inner_text().strip().split('\n')[0]
        
        # Filtres grossiers pour éviter les faux-positifs
        if not name or len(name) < 3:
            continue
            
        slug = slugify(name)
        
        if slug in seen:
            continue
        seen.add(slug)
        
        # Déduction de la date : 
        # Si la date n'est pas dans le noeud A, on se rabat sur la date du Scraping
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        campaigns.append({
            "slug": slug,
            "name": name,
            "date": date_str,
            "url": full_url,
            "source": "futbin"
        })
        
    return campaigns

def main():
    setup_directories()
    logging.info("🚀 Démarrage du Scraper : Index des Campagnes FUTBIN")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 🛡️ Masquer Playwright pour Cloudflare
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        try:
            logging.info(f"Navigate to {BASE_URL}")
            page.goto(BASE_URL, wait_until="domcontentloaded", timeout=45000)
            
            # Attente de la réhydratation JS de FUTBIN
            page.wait_for_timeout(3000)
            
            # Petit scroll pour trigger le lazy loading des grilles de squads
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            
        except TimeoutError:
            logging.error("❌ Timeout FUTBIN. Le site est lent ou bloque Playwright.")
            browser.close()
            return

        campaigns = extract_campaigns(page)
        browser.close()

    if not campaigns:
        logging.warning("⚠️ Aucune campagne extraite ! Vérifiez le sélecteur `a[href*='/squad/']` sur le navigateur.")
        return

    logging.info(f"✅ Extrait : {len(campaigns)} campagnes.")
    
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(campaigns, f, indent=2, ensure_ascii=False)
        
    logging.info(f"📁 Sauvegarde terminée : {OUT_JSON}")

if __name__ == "__main__":
    main()
