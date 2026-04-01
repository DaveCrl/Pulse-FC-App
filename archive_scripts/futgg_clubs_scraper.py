import os
import re
import json
import time
import requests
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.fut.gg/clubs/"
OUT_DIR = "club_icons"
JSON_FILE = "clubs.json"

os.makedirs(OUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
})

def slugify(text: str) -> str:
    text = text.strip().lower()
    replacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a", "ä": "a",
        "î": "i", "ï": "i",
        "ô": "o", "ö": "o",
        "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
        "œ": "oe",
        "’": "'"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text

def guess_extension(url: str) -> str:
    path = urlparse(url).path.lower()
    _, ext = os.path.splitext(path)
    return ext if ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"] else ".png"

def download_file(url: str, filepath: str) -> bool:
    try:
        r = session.get(url, timeout=30)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"[ERR DOWNLOAD] {url} -> {e}")
        return False

def main():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 2200})
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)

        page.mouse.wheel(0, 4000)
        page.wait_for_timeout(1500)

        links = page.locator('a[href*="/clubs/"]')
        count = links.count()
        seen = set()

        for i in range(count):
            item = links.nth(i)
            href = item.get_attribute("href")
            if not href:
                continue

            full_url = urljoin(BASE_URL, href)

            if full_url.rstrip("/") == BASE_URL.rstrip("/"):
                continue

            if full_url in seen:
                continue
            seen.add(full_url)

            text = item.inner_text().strip()
            text = re.sub(r"\s+", " ", text).strip()

            imgs = item.locator("img")
            img_url = None
            for j in range(imgs.count()):
                src = imgs.nth(j).get_attribute("src")
                if src and src.startswith("http"):
                    img_url = src
                    break

            if not text or not img_url:
                continue

            ext = guess_extension(img_url)
            filename = f"{slugify(text)}{ext}"
            filepath = os.path.join(OUT_DIR, filename)

            if download_file(img_url, filepath):
                results.append({
                    "slug": slugify(text),
                    "name": text,
                    "icon": f"/assets/clubs/{filename}",
                    "icon_filename": filename,
                    "source_url": full_url,
                    "source_icon_url": img_url
                })
                print(f"[OK] {text}")

            time.sleep(0.15)

        browser.close()

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nTerminé : {len(results)} clubs")
    print(f"Dossier : {OUT_DIR}")
    print(f"JSON : {JSON_FILE}")

if __name__ == "__main__":
    main()