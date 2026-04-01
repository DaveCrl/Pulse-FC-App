#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

print("Cherche Momitala...")

with open('/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/src/data/players_clean.json', encoding='utf-8') as f:
    players = json.load(f)

found = False
for p in players:
    if 'momitala' in p.get('nom', '').lower():
        found = True
        print(f"\n✓ Trouvé: {p['nom']}")
        print(f"  Rarete: {p.get('rarete')}")
        print(f"  Club: {p.get('club')}")
        print(f"  Playstyles: {p.get('playstyles', [])}")
        print(f"  Playstyles Plus: {p.get('playstyles_plus', [])}")

if not found:
    print("Momitala non trouvé, affichage des premiers playstyles trouvés:")
    for p in players[:10]:
        if p.get('playstyles') or p.get('playstyles_plus'):
            print(f"\n  {p.get('nom')}:")
            print(f"    Playstyles: {p.get('playstyles', [])}")
            print(f"    Playstyles Plus: {p.get('playstyles_plus', [])}")
