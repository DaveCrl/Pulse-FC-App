#!/usr/bin/env python3
import json
import re

# Define all playstyle replacements
playstyle_replacements = {
    # Foulée rapide replacements
    'Pas Rapide': 'Foulée rapide',
    'Pas Rapide+': 'Foulée rapide+',
    'Rapide': 'Foulée rapide',
    'Rapide+': 'Foulée rapide+',
    
    # Passe Fusante replacements
    'Passe précise': 'Passe fusante',
    'Passe précise+': 'Passe fusante+',
    
    # Freineur → Technicien
    'Freineur': 'Technicien',
    'Freineur+': 'Technicien+',
    
    # Longue Passe → Passe longue
    'Longue Passe': 'Passe longue',
    'Longue Passe+': 'Passe longue+',
    
    # Pressing Éprouvé → Résiste au pressing
    'Pressing Éprouvé': 'Résiste au pressing',
    'Pressing Éprouvé+': 'Résiste au pressing+',
    'Pressing': 'Résiste au pressing',
    'Pressing+': 'Résiste au pressing+',
    
    # Tête de précision → Tête précise
    'Tête de précision': 'Tête précise',
    'Tête de précision+': 'Tête précise+',
    
    # Tir lobé → Ballon piqué
    'Tir lobé': 'Ballon piqué',
    'Tir lobe': 'Ballon piqué',
    'Tir lobé+': 'Ballon piqué+',
    'Tir lobe+': 'Ballon piqué+',
    
    # Implacable → Infatigable
    'Implacable': 'Infatigable',
    'Implacable+': 'Infatigable+',
    
    # Deflecteur → Déviation
    'Deflecteur': 'Déviation',
    'Deflecteur+': 'Déviation+',
    
    # Jeu de pieds → Arrêts du pied
    'Jeu de pieds': 'Arrêts du pied',
    'Jeu de pieds+': 'Arrêts du pied+',
    
    # Sortie Rapide → Sort du but
    'Sortie Rapide': 'Sort du but',
    'Sortie Rapide+': 'Sort du but+',
    'Sortie rapide': 'Sort du but',
    'Sortie rapide+': 'Sort du but+',
    
    # Marquage → Lutte
    'Marquage': 'Lutte',
    'Marquage+': 'Lutte+',
    
    # Blocage → Contre
    'Blocage': 'Contre',
    'Blocage+': 'Contre+',
    
    # Grande relance → Longue relance
    'Grande relance': 'Longue relance',
    'Grande relance+': 'Longue relance+',
    
    # Maitre des centre → Sortie sur les centres
    'Maitre des centre': 'Sortie sur les centres',
    'Maitre des centre+': 'Sortie sur les centres+',
    'Maître des centres': 'Sortie sur les centres',
    'Maître des centres+': 'Sortie sur les centres+',
    
    # Grande envergure → Arrêt de loin
    'Grande envergure': 'Arrêt de loin',
    'Grande envergure+': 'Arrêt de loin+',
    
    # Tir Enroulé → Tir en finesse (already done, but including for completeness)
    'Tir Enroulé': 'Tir en finesse',
    'Tir Enroulé+': 'Tir en finesse+',
    
    # Passe Fouettée → Passe travaillée (already done)
    'Passe Fouettée': 'Passe travaillée',
    'Passe Fouettée+': 'Passe travaillée+',
}

def fix_playstyles_in_file(filepath):
    """Fix all playstyle replacements in the JSON file"""
    print(f"Loading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_changes = 0
    
    print(f"Processing {len(data)} players...")
    
    for player in data:
        if 'playstyles' in player and player['playstyles']:
            original_playstyles = player['playstyles'].copy()
            new_playstyles = []
            
            for ps in player['playstyles']:
                if ps in playstyle_replacements:
                    new_ps = playstyle_replacements[ps]
                    new_playstyles.append(new_ps)
                    if new_ps != ps:
                        total_changes += 1
                        print(f"  {player.get('nom', 'Unknown')}: '{ps}' → '{new_ps}'")
                else:
                    new_playstyles.append(ps)
            
            player['playstyles'] = new_playstyles
    
    print(f"\nSaving {filepath}...")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    
    print(f"\n✓ Total changes made: {total_changes}")
    return len(data), total_changes

# Run on all data files
files_to_process = [
    '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_merged.json',
]

for filepath in files_to_process:
    try:
        player_count, change_count = fix_playstyles_in_file(filepath)
        print(f"✓ Processed {player_count} players with {change_count} playstyle changes\n")
    except Exception as e:
        print(f"Error processing {filepath}: {e}\n")
