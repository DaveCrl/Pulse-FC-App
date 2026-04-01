#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys

# Mapping des corrections de playstyles
corrections = {
    "Pas Rapide+": "Rapide +",
    "Tir Enroulé": "Tir en finesse",
    "Premier Contact": "Contrôle",
    "Décisif": "Révolutionnaire"
}

def fix_playstyles(input_file, output_file=None):
    """Corriger les playstyles dans la base de données"""
    if output_file is None:
        output_file = input_file
    
    # Lire le fichier
    print(f"📖 Lecture du fichier: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    print(f"✓ Fichier chargé: {len(players)} joueurs")
    
    # Compter les modifications
    total_modified = 0
    mbappé_found = False
    
    # Appliquer les corrections
    for player in players:
        if 'playstyles' in player and isinstance(player['playstyles'], list):
            original = player['playstyles'].copy()
            player['playstyles'] = [corrections.get(ps, ps) for ps in player['playstyles']]
            
            # Vérifier si des modifications ont été faites
            if original != player['playstyles']:
                total_modified += 1
                if 'Mbappé' in player.get('nom', ''):
                    mbappé_found = True
                    print(f"\n✓ {player['nom']} ({player.get('rarete', 'N/A')}) - Playstyles corrigés:")
                    print(f"  Avant: {original}")
                    print(f"  Après: {player['playstyles']}")
    
    # Sauvegarder
    print(f"\n💾 Sauvegarde du fichier: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)
    
    # Statistiques
    print(f"\n" + "="*50)
    print(f"📊 STATISTIQUES DE CORRECTION")
    print(f"="*50)
    print(f"✓ Total de joueurs modifiés: {total_modified}")
    print(f"✓ Mbappé trouvé et modifié: {mbappé_found}")
    print(f"✅ Fichier sauvegardé avec succès!")
    
    return total_modified, mbappé_found

if __name__ == "__main__":
    input_path = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/src/data/players_clean.json'
    fix_playstyles(input_path)
