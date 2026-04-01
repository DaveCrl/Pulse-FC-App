#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

base_path = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0'

files_to_check = [
    f'{base_path}/src/data/players_clean.json',
    f'{base_path}/players_merged.json',
    f'{base_path}/data/campaign_players.json',
]

print("=" * 70)
print("VÉRIFICATION FINALE DES PLAYSTYLES CORRIGÉS")
print("=" * 70)

for file_path in files_to_check:
    if not os.path.exists(file_path):
        print(f"\n⚠️  Fichier non trouvé: {file_path}")
        continue
    
    print(f"\n📖 Vérification: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        found = False
        for item in data:
            if isinstance(item, dict) and 'nom' in item:
                if 'mbapp' in item.get('nom', '').lower():
                    print(f"  ✓ Trouvé: {item['nom']}")
                    playstyles = item.get('playstyles', [])
                    print(f"    Playstyles: {playstyles}")
                    
                    # Vérifier chaque playstyle
                    print(f"    Vérifications:")
                    checks = {
                        'Rapide+': 'Rapide+' in playstyles,
                        'Acrobatique': 'Acrobatique' in playstyles,
                        'Tir en finesse': 'Tir en finesse' in playstyles,
                        'Contrôle': 'Contrôle' in playstyles,
                        'Révolutionnaire': 'Révolutionnaire' in playstyles,
                        'Tir Rasant': 'Tir Rasant' in playstyles,
                        'Rapide': 'Rapide' in playstyles,
                    }
                    
                    for name, status in checks.items():
                        status_icon = "✅" if status else "❌"
                        print(f"      {status_icon} {name}")
                    
                    found = True
                    break
        
        if not found:
            print("  ℹ️  Mbappé non trouvé dans ce fichier")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")

print("\n" + "=" * 70)
print("✅ VÉRIFICATION TERMINÉE!")
print("=" * 70)
