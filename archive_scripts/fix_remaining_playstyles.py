#!/usr/bin/env python3
import json

# Fix remaining playstyle names and capitalizations
additional_replacements = {
    # Fix case sensitivity issues
    'Forteresse Aérienne': 'Forteresse aérienne',
    'Forteresse Aérienne+': 'Forteresse aérienne+',
    'Tête de Précision': 'Tête précise',
    'Tête de Précision+': 'Tête précise+',
    'Tacle Glissé': 'Tacle glissé',
    'Tacle Glissé+': 'Tacle glissé+',
    'Passe Incisive': 'Passe incisive',
    'Passe Incisive+': 'Passe incisive+',
    'Coup de Pied Arrêté': 'Coup de pied arrêté',
    'Coup de Pied Arrêté+': 'Coup de pied arrêté+',
    'Tir Puissant': 'Tir puissant',
    'Tir Puissant+': 'Tir puissant+',
    'Tir Rasant': 'Tir rasant appuyé',
    'Tir Rasant+': 'Tir rasant appuyé+',
    'Maître des Centres': 'Sortie sur les centres',
    'Maître des Centres+': 'Sortie sur les centres+',
    'Grande Relance': 'Longue relance',
    'Grande Relance+': 'Longue relance+',
    'Passe Précise': 'Passe fusante',
    'Passe Précise+': 'Passe fusante+',
    'Tiki Taka': 'Tiki-taka',
    'Tiki Taka+': 'Tiki-taka+',
    'Jeu de Pieds': 'Arrêts du pied',
    'Jeu de Pieds+': 'Arrêts du pied+',
    'Feinteur': 'Technicien',
    'Feinteur+': 'Technicien+',
    'Déflecteur': 'Déviation',
    'Déflecteur+': 'Déviation+',
    'Grande Envergure': 'Arrêt de loin',
    'Grande Envergure+': 'Arrêt de loin+',
    'Costaud': 'Agressif',
    'Costaud+': 'Agressif+',
    'Longue Relance': 'Longue relance',
    'Longue Relance+': 'Longue relance+',
    'Révolutionnaire': 'Renversement',
    'Imposant': 'Passage en force',
    'Imposant+': 'Passage en force+',
    'Tir Lobé': 'Ballon piqué',
    'Tir lobe': 'Ballon piqué',
    'Tir Lobé+': 'Ballon piqué+',
    'Tir lobe+': 'Ballon piqué+',
}

filename = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_merged.json'

print(f"Loading {filename}...")
with open(filename, 'r', encoding='utf-8') as f:
    players = json.load(f)

total_changes = 0

print(f"Processing {len(players)} players...")

for player in players:
    if 'playstyles' in player and player['playstyles']:
        new_playstyles = []
        
        for ps in player['playstyles']:
            if ps in additional_replacements:
                new_ps = additional_replacements[ps]
                new_playstyles.append(new_ps)
                if new_ps != ps:
                    total_changes += 1
                    if total_changes <= 50:  # Print first 50
                        print(f"  {player.get('nom', 'Unknown')}: '{ps}' → '{new_ps}'")
            else:
                new_playstyles.append(ps)
        
        player['playstyles'] = new_playstyles

print(f"\nSaving {filename}...")
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(players, f, ensure_ascii=False)

print(f"\n✓ Total changes made: {total_changes}")
