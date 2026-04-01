#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FC Pulse — Scraper Nations (FUTBIN)
Récupère les nations/pays de FUTBIN
OUTPUT : nations.json

Usage :
    pip3 install requests beautifulsoup4
    python3 scrape_nations.py
"""

import requests
import json
import time
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup

BASE        = "https://www.futbin.com"
DELAY       = 1
HEADERS     = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def get(url, retries=3):
    """Requête GET avec retry automatique."""
    for attempt in range(retries):
        try:
            r = SESSION.get(url, timeout=15)
            r.raise_for_status()
            time.sleep(DELAY)
            return BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            print(f"  ⚠ Tentative {attempt+1}/{retries} échouée: {e}")
            time.sleep(DELAY * 2)
    print(f"  ❌ Impossible de récupérer : {url}")
    return None

def clean(text):
    """Nettoie le texte."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def scrape_nations_futbin():
    """Scrape les nations depuis FUTBIN."""
    print("🌍 Scraping des nations depuis FUTBIN...")
    
    url = f"{BASE}/nations"
    soup = get(url)
    
    if not soup:
        print("❌ Impossible de charger la page des nations")
        return []
    
    nations = []
    
    # Chercher les liens contenant "nations"
    for link in soup.find_all("a"):
        href = link.get("href", "")
        
        # Chercher les liens de nations
        if "/nations/" in href and len(href) > len("/nations/"):
            name = clean(link.get_text())
            
            if not name or name.lower() == "nations":
                continue
            
            slug = href.rstrip("/").split("/")[-1]
            
            if not slug:
                continue
            
            nation = {
                "name": name,
                "slug": slug,
                "url": BASE + href if href.startswith("/") else href,
            }
            
            # Chercher une image
            img = link.find("img")
            if img and img.get("src"):
                nation["flag"] = img["src"]
            
            # Vérifier si on a déjà cette nation
            if not any(n["slug"] == slug for n in nations):
                nations.append(nation)
                print(f"  ✓ {name} ({slug})")
    
    return nations

def scrape_nations_fut_gg_api():
    """Essayer de scraper FUT.GG avec une approche API."""
    print("🌍 Essai FUT.GG (API)...")
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    
    try:
        endpoints = [
            "https://api.fut.gg/nations",
            "https://www.fut.gg/api/nations",
            "https://www.fut.gg/data/nations.json",
        ]
        
        for endpoint in endpoints:
            try:
                r = requests.get(endpoint, headers=headers, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    print(f"✓ Données trouvées sur {endpoint}")
                    return data if isinstance(data, list) else data.get("nations", [])
            except:
                continue
    except Exception as e:
        print(f"  ⚠ Erreur: {e}")
    
    return []

def main():
    """Fonction principale."""
    print("=" * 60)
    print("FC PULSE — SCRAPER NATIONS")
    print("=" * 60)
    
    # Essayer FUT.GG d'abord (API)
    nations = scrape_nations_fut_gg_api()
    
    # Sinon, utiliser FUTBIN
    if not nations:
        nations = scrape_nations_futbin()
    
    if not nations:
        print("❌ Aucune nation trouvée")
        return
    
    # Sauvegarder
    output_file = "nations.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(nations, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(nations)} nations sauvegardées dans {output_file}")
    print(f"   Taille du fichier: {os.path.getsize(output_file)} bytes")
    
    # Afficher un échantillon
    print("\n📋 Échantillon:")
    for nation in nations[:5]:
        print(f"  - {nation.get('name')} ({nation.get('slug')})")

if __name__ == "__main__":
    main()
