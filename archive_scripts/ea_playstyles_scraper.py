import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.ea.com/fr/games/ea-sports-fc/ratings"
OUTPUT_DIR = "ea_playstyles_plus_icons"
JSON_FILE = "ea_playstyles_plus.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Referer": "https://www.ea.com/"
})


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = text.replace("+", " plus ")
    replacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a", "ä": "a",
        "î": "i", "ï": "i",
        "ô": "o", "ö": "o",
        "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
        "œ": "oe",
        "’": "'", "“": '"', "”": '"'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text


def get_soup(url: str):
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except requests.RequestException as e:
        print(f"[ERREUR] Impossible de charger {url} -> {e}")
        return None


def clean_drop_assets_url(url: str) -> str:
    """
    Garde une vraie URL image exploitable.
    Si l'URL a des params de resize/q, on les remplace par une version propre.
    """
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # On force une version HD cohérente
    return f"{base}?im=Resize=(2560)&q=80"


def pick_best_src_from_picture(picture_tag) -> str | None:
    """
    Cherche la meilleure URL drop-assets dans:
    1. img[src]
    2. source[srcset]
    """
    if picture_tag is None:
        return None

    img = picture_tag.find("img", src=True)
    if img and "drop-assets.ea.com" in img["src"]:
        return clean_drop_assets_url(img["src"])

    for source in picture_tag.find_all("source", srcset=True):
        srcset = source["srcset"]
        candidates = [part.strip().split(" ")[0] for part in srcset.split(",")]
        drop_candidates = [c for c in candidates if "drop-assets.ea.com" in c]
        if drop_candidates:
            # On prend la plus grande version présente dans le srcset si possible
            best = None
            best_score = -1
            for candidate in drop_candidates:
                score = 0
                m = re.search(r"Resize=\((\d+)\)", candidate)
                if m:
                    score = int(m.group(1))
                if score > best_score:
                    best_score = score
                    best = candidate
            return clean_drop_assets_url(best)

    return None


def collect_playstyles_plus():
    soup = get_soup(BASE_URL)
    if soup is None:
        return []

    results = []
    seen_pages = set()

    # On cible toutes les cartes dont le href contient /play-style-plus/
    for a in soup.select('a[href*="/play-style-plus/"]'):
        href = a.get("href", "").strip()
        page_url = urljoin(BASE_URL, href)

        if page_url in seen_pages:
            continue
        seen_pages.add(page_url)

        label_node = a.find(class_=re.compile(r"ItemCard_label"))
        label = label_node.get_text(" ", strip=True) if label_node else a.get_text(" ", strip=True)

        picture = a.find("picture")
        icon_url = pick_best_src_from_picture(picture)

        if not icon_url or "drop-assets.ea.com" not in icon_url:
            continue

        results.append({
            "label": label.strip(),
            "page_url": page_url,
            "icon_url": icon_url,
            "is_plus": True
        })

    return results


def guess_extension(file_url: str) -> str:
    path = urlparse(file_url).path.lower()
    _, ext = os.path.splitext(path)
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]:
        return ext
    return ".png"


def download_file(url: str, filepath: str) -> bool:
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        return True
    except requests.RequestException as e:
        print(f"[ERREUR DOWNLOAD] {url} -> {e}")
        return False


def main():
    items = collect_playstyles_plus()
    print(f"{len(items)} PlayStyle+ trouvés")

    exported = []

    for item in items:
        label = item["label"]
        icon_url = item["icon_url"]

        ext = guess_extension(icon_url)
        filename = f"{slugify(label)}{ext}"
        filepath = os.path.join(OUTPUT_DIR, filename)

        ok = download_file(icon_url, filepath)
        if ok:
            item["filename"] = filename
            item["local_path"] = filepath
            exported.append(item)
            print(f"[OK] {label} -> {filepath}")
            print(f"     {icon_url}")
        else:
            print(f"[ERR] {label}")

        time.sleep(0.35)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(exported, f, ensure_ascii=False, indent=2)

    print("\nTerminé.")
    print(f"Images: {len(exported)}")
    print(f"Dossier: {OUTPUT_DIR}")
    print(f"JSON: {JSON_FILE}")


if __name__ == "__main__":
    main()
