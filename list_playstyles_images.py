#!/usr/bin/env python3
"""
Generate complete list of playstyles images
"""

import os
import csv

# Directories
playstyles_dir = 'public/assets/playstyles'
playstyles_plus_dir = 'public/assets/playstyles_plus'
archive_plus_dir = 'archive_assets/ea_playstyles_plus_icons'

# Get files
playstyles_files = sorted([f for f in os.listdir(playstyles_dir) if f.endswith('.png')])
playstyles_plus_files = sorted([f for f in os.listdir(playstyles_plus_dir) if f.endswith('.png')])
archive_plus_files = sorted([f for f in os.listdir(archive_plus_dir) if f.endswith('.png')])

# Mapping from filename to French names (from data)
# Based on the playstyles with +
playstyle_names = {
    # Playstyles+
    'acrobatique-plus': 'Acrobatique+',
    'ballon-pique-plus': 'Ballon piqué+',
    'coup-de-pied-arrete-plus': 'Coups de pied arrêtés+',
    'tete-precise-plus': 'Tête précise+',
    'tir-en-finesse-plus': 'Tir en finesse+',
    'tir-puissant-plus': 'Tir puissant+',
    'tir-rasant-appuye-plus': 'Tir rasant appuyé+',
    
    # Playstyles
    'acrobatique': 'Acrobatique',
    'agressif': 'Agressif',
    'anticipation': 'Anticipation',
    'arret-du-pied': 'Arrêt du pied',
    'ballon-pique': 'Ballon piqué',
    'classe-de-loin': 'Classe de loin',
    'contre': 'Contre',
    'controle': 'Contrôle',
    'coup-de-pied-arrete': 'Coups de pied arrêtés',
    'deflector': 'Déviation',
    'fantaisiste': 'Fantaisiste',
    'forteresse-aerienne': 'Forteresse aérienne',
    'foulee-rapide': 'Foulée rapide',
    'infatigable': 'Infatigable',
    'interception': 'Interception',
    'longue-relance': 'Longue relance',
    'longue-touche': 'Longue touche',
    'lutte': 'Lutte',
    'passage-en-force': 'Passage en force',
    'passe-en-profondeur': 'Passe en profondeur',
    'passe-incisive': 'Passe incisive',
    'passe-longue': 'Passe longue',
    'passe-tendue': 'Passe tendue',
    'passe-travaillee': 'Passe travaillée',
    'rapide': 'Rapide',
    'renversement': 'Renversement',
    'resiste-au-pressing': 'Résiste au pressing',
    'sort-du-but': 'Sort du but',
    'sortie-sur-les-centres': 'Sortie sur les centres',
    'tacle-glisse': 'Tacle glissé',
    'technicien': 'Technicien',
    'technique': 'Technique',
    'tete-precise': 'Tête précise',
    'tiki-taka': 'Tiki-Taka',
    'tir-en-finesse': 'Tir en finesse',
    'tir-puissant': 'Tir puissant',
    'tir-rasant-appuye': 'Tir rasant appuyé',
    'revolutionnaire': 'Révolutionnaire',
    'passe-tendue': 'Passe tendue',
    'allonge': 'Allonge',
}

print("\n" + "="*80)
print("PLAYSTYLES IMAGES - COMPLETE LIST")
print("="*80 + "\n")

# Create CSV
csv_file = 'playstyles_images_list.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Type', 'Playstyle Name', 'Image Filename', 'Path'])
    
    # Playstyles+
    for img_file in playstyles_plus_files:
        filename_base = img_file.replace('.png', '')
        name = playstyle_names.get(filename_base, filename_base.replace('-', ' ').title())
        writer.writerow(['playstyles+', name, img_file, f'/assets/playstyles_plus/{img_file}'])
    
    # Playstyles
    for img_file in playstyles_files:
        filename_base = img_file.replace('.png', '')
        name = playstyle_names.get(filename_base, filename_base.replace('-', ' ').title())
        writer.writerow(['playstyles', name, img_file, f'/assets/playstyles/{img_file}'])

print(f"✓ CSV generated: {csv_file}\n")

print("PLAYSTYLES+ IMAGES (in public/assets/playstyles_plus/):")
print("-" * 80)
for i, f in enumerate(playstyles_plus_files, 1):
    base = f.replace('.png', '')
    name = playstyle_names.get(base, base.replace('-', ' ').title())
    print(f"{i:2d}. {name:30s} → {f}")

print(f"\nTotal: {len(playstyles_plus_files)} images\n")

print("PLAYSTYLES IMAGES (in public/assets/playstyles/):")
print("-" * 80)
for i, f in enumerate(playstyles_files, 1):
    base = f.replace('.png', '')
    name = playstyle_names.get(base, base.replace('-', ' ').title())
    print(f"{i:2d}. {name:30s} → {f}")

print(f"\nTotal: {len(playstyles_files)} images\n")

print("="*80)
print(f"SUMMARY:")
print(f"  Playstyles+ images: {len(playstyles_plus_files)}")
print(f"  Playstyles images: {len(playstyles_files)}")
print(f"  Archive playstyles+ images: {len(archive_plus_files)}")
print(f"  TOTAL UNIQUE IMAGES: {len(playstyles_plus_files) + len(playstyles_files)}")
print("="*80 + "\n")
