#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

corrections = {
    "Pas Rapide+": "Rapide+",
    "Tir Enroulé": "Tir en finesse", 
    "Premier Contact": "Contrôle",
    "Décisif": "Révolutionnaire"
}

base_path = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0'

files_to_fix = [
    f'{base_path}/players_merged.json',
    f'{base_path}/data/campaign_players.json',
]

print("=" * 60)
print("CORRECTION DES FICHIERS SUPPLÉMENTAIRES")
print("=" * 60)

for file_path in files_to_fix:
    if not os.path.exists(file_path):
        print(f"\n⚠️  Fichier non trouvé: {file_path}")
        continue
    
    try:
        print(f"\n📖 Traitement: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = 0
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'playstyles' in item and isinstance(item['playstyles'], list):
                    original = item['playstyles'].copy()
                    item['playstyles'] = [corrections.get(ps, ps) for ps in item['playstyles']]
                    if original != item['playstyles']:
                        modified += 1
        
        if modified > 0:
            print(f"✓ {modified} joueurs corrigés")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Fichier sauvegardé!")
        else:
            print(f"ℹ️  Aucune modification nécessaire")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

print("\n" + "=" * 60)
print("✅ CORRECTION TERMINÉE!")
print("=" * 60)
