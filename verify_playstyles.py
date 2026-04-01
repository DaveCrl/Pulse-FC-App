#!/usr/bin/env python3
import json
from collections import defaultdict

# Playstyle to image mapping
playstyle_images = {
    'Tir rasant appuyé': 'tir-rasant-appuye',
    'Tête précise': 'tete-precise',
    'Acrobatique': 'acrobatique',
    'Tir en finesse': 'tir-en-finesse',
    'Ballon piqué': 'ballon-pique',
    'Tir puissant': 'tir-puissant',
    'Coup de pied arrêté': 'coup-de-pied-arrete',
    'Technique': 'technique',
    'Foulée rapide': 'foulee-rapide',
    'Contrôle': 'controle',
    'Technicien': 'technicien',
    'Résiste au pressing': 'resiste-au-pressing',
    'Forteresse aérienne': 'forteresse-aerienne',
    'Lutte': 'lutte',
    'Contre': 'contre',
    'Interception': 'interception',
    'Anticipation': 'anticipation',
    'Tacle glissé': 'tacle-glisse',
    'Renversement': 'renversement',
    'Sort du but': 'sort-du-but',
    'Longue relance': 'longue-relance',
    'Arrêt du pied': 'arret-du-pied',
    'Sortie sur les centres': 'sortie-sur-les-centres',
    'Classe de loin': 'classe-de-loin',
    'Déviation': 'deflector',
    'Fantaisiste': 'fantaisiste',
    'Passe incisive': 'passe-incisive',
    'Passe en profondeur': 'passe-en-profondeur',
    'Passe longue': 'passe-longue',
    'Tiki-taka': 'tiki-taka',
    'Passe travaillée': 'passe-travaillee',
    'Passage en force': 'passage-en-force',
    'Agressif': 'agressif',
    'Infatigable': 'infatigable',
    'Longue touche': 'longue-touche',
    'Premier Contact': 'premier-contact',
    'Décisif': 'decisif',
    'Inventif': 'inventif',
    'Distribution': 'distribution',
    'Arrêts du pied': 'arret-du-pied',
    'Passe fusante': 'passe-en-profondeur',
    'Freineur': 'technicien',
    'Arrêt de loin': 'classe-de-loin',
}

filename = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_merged.json'

print("Loading player data...")
with open(filename, 'r', encoding='utf-8') as f:
    players = json.load(f)

# Count playstyles
playstyle_count = defaultdict(int)
players_with_playstyle = defaultdict(list)

for player in players:
    if 'playstyles' in player and player['playstyles']:
        for ps in player['playstyles']:
            playstyle_count[ps] += 1
            players_with_playstyle[ps].append(player.get('nom', 'Unknown'))

print("\n" + "="*80)
print("PLAYSTYLE ANALYSIS")
print("="*80)

# Sort by frequency
sorted_playstyles = sorted(playstyle_count.items(), key=lambda x: x[1], reverse=True)

print(f"\nTotal unique playstyles: {len(sorted_playstyles)}")
print(f"Total playstyle occurrences: {sum(playstyle_count.values())}")

print("\n" + "-"*80)
print("PLAYSTYLES WITH MISSING IMAGES:")
print("-"*80)

missing_images = []
for ps, count in sorted_playstyles:
    # Check if it's a + variant
    ps_base = ps.rstrip('+').strip()
    
    if ps_base not in playstyle_images and ps not in playstyle_images:
        missing_images.append((ps, count))
        print(f"❌ '{ps}' (appears {count} times)")
        if count <= 5:
            print(f"   Players: {', '.join(players_with_playstyle[ps][:5])}")

if not missing_images:
    print("✓ All playstyles have image mappings!")

print("\n" + "-"*80)
print("ALL PLAYSTYLES (TOP 50):")
print("-"*80)

for ps, count in sorted_playstyles[:50]:
    ps_base = ps.rstrip('+').strip()
    is_plus = ps.endswith('+')
    has_mapping = ps in playstyle_images or ps_base in playstyle_images
    status = "✓" if has_mapping else "❌"
    
    image_name = playstyle_images.get(ps) or playstyle_images.get(ps_base)
    image_info = f" → {image_name}.png" if image_name else " → NO IMAGE"
    
    print(f"{status} {ps:40} ({count:5} players){image_info}")

print("\n" + "-"*80)
print("SUMMARY FOR VERIFICATION:")
print("-"*80)
print(f"\nTotal playstyles found: {len(sorted_playstyles)}")
print(f"Playstyles without images: {len(missing_images)}")
if missing_images:
    print("\nMissing image mappings for:")
    for ps, count in missing_images:
        print(f"  - {ps}")
