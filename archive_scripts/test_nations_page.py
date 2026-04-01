#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

HEADERS     = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
}

try:
    r = requests.get("https://www.fut.gg/nations/", headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Analyser la structure
    print("Analyse de la structure HTML...")
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers.get('content-type')}")
    
    # Chercher div ou section avec "nation" dans le nom
    for elem in soup.find_all(["div", "section"], class_=re.compile("nation", re.I)):
        print(f"\nFound: {elem.name} class='{elem.get('class')}'")
        print(elem.prettify()[:500])
        print("...")
        break
    
    # Chercher tous les liens
    print("\n\nTous les liens de la page:")
    for link in soup.find_all("a", limit=20):
        href = link.get("href", "")
        text = link.get_text()[:50]
        if "nation" in href.lower():
            print(f"  {href} -> {text}")
    
except Exception as e:
    print(f"Erreur: {e}")
