#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys

corrections = {
    "Pas Rapide+": "Rapide+",
    "Tir Enroulé": "Tir en finesse",
    "Premier Contact": "Contrôle",
    "Décisif": "Révolutionnaire"
}

file_path = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/data/campaign_players.json'

print(f"📖 Traitement: {file_path}")

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ Fichier chargé: {len(data)} éléments")

modified = 0
for item in data:
    if isinstance(item, dict) and 'playstyles' in item and isinstance(item['playstyles'], list):
        original = item['playstyles'].copy()
        item['playstyles'] = [corrections.get(ps, ps) for ps in item['playstyles']]
        if original != item['playstyles']:
            modified += 1

print(f"✓ {modified} joueurs corrigés")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Fichier sauvegardé!")

# Vérifier Mbappé
found = False
for item in data:
    if 'mbapp' in item.get('nom', '').lower():
        print(f"\n✓ Vérification Mbappé dans campaign_players.json:")
        print(f"  {item['nom']}: {item.get('playstyles', [])}")
        found = True

if not found:
    print("\nℹ️  Mbappé non trouvé dans campaign_players.json")
