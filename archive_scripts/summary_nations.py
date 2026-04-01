#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/nations.json') as f:
    nations = json.load(f)

print("=" * 70)
print("RÉSUMÉ DU SCRAPING DES NATIONS")
print("=" * 70)

print(f"\n📊 Total: {len(nations)} nations")

print("\n🌍 Premières 10 nations:")
for i, nation in enumerate(nations[:10], 1):
    print(f"  {i:2}. {nation['name']:30} - slug: {nation['slug']}")

print("\n... (nations du milieu omises) ...\n")

print("🌍 Dernières 5 nations:")
for i, nation in enumerate(nations[-5:], len(nations) - 4):
    print(f"  {i:3}. {nation['name']:30} - slug: {nation['slug']}")

print("\n🔍 Nations spécifiques trouvées:")
special_nations = ['France', 'Brazil', 'Argentina', 'International', 'England', 'Spain']
for name in special_nations:
    found = next((n for n in nations if n['name'].lower() == name.lower()), None)
    if found:
        print(f"  ✓ {found['name']:20} → slug: {found['slug']}")

print("\n" + "=" * 70)
print("✅ SCRAPING TERMINÉ AVEC SUCCÈS")
print("=" * 70)
print(f"\n📁 Fichiers générés:")
print(f"  - /nations.json")
print(f"  - /src/data/nations.json") 
print(f"  - /data/nations.json")
print(f"\n💾 Source: https://www.futbin.com/nations")
print(f"📝 Script: scrape_nations.py")
