#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

corrections = {
    "Inventif": "Technicien",
    "Inventif+": "Technicien+",
}

base_path = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0'

files_to_fix = [
    f'{base_path}/src/data/players_clean.json',
    f'{base_path}/players_merged.json',
]

print("=" * 60)
print("CORRECTION DES PLAYSTYLES")
print("=" * 60)

for file_path in files_to_fix:
    print(f"\n📖 Traitement: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = 0
    for player in data:
        if 'playstyles' in player and isinstance(player['playstyles'], list):
            original = player['playstyles'].copy()
            player['playstyles'] = [corrections.get(ps, ps) for ps in player['playstyles']]
            if original != player['playstyles']:
                modified += 1
    
    print(f"✓ {modified} joueurs corrigés")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Fichier sauvegardé!")

print("\n" + "=" * 60)
print("✅ CORRECTION TERMINÉE!")
print("=" * 60)
