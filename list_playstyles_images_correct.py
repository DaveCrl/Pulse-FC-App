#!/usr/bin/env python3
"""
Generate CORRECT list of playstyles images with proper mapping
"""

import os
import csv

# Mapping from French name to filenames
PLAYSTYLES_MAPPING = {
    "Acrobatique": "acrobatique.png",
    "Agressif": "agressif.png",
    "Allonge": None,  # No image found
    "Anticipation": "anticipation.png",
    "Arrêt du pied": "arret-du-pied.png",
    "Ballon piqué": "ballon-pique.png",
    "Contre": "contre.png",
    "Contrôle": "controle.png",
    "Coups de pied arrêtés": "coup-de-pied-arrete.png",
    "Déviation": "deflector.png",
    "Fantaisiste": "fantaisiste.png",
    "Forteresse aérienne": "forteresse-aerienne.png",
    "Foulée rapide": "foulee-rapide.png",
    "Infatigable": "infatigable.png",
    "Interception": "interception.png",
    "Longue relance": "longue-relance.png",
    "Longue touche": "longue-touche.png",
    "Lutte": "lutte.png",
    "Passage en force": "passage-en-force.png",
    "Passe incisive": "passe-incisive.png",
    "Passe longue": "passe-longue.png",
    "Passe tendue": "passe-tendue.png",
    "Passe travaillée": "passe-travaillee.png",
    "Rapide": "rapide.png",
    "Résiste au pressing": "resiste-au-pressing.png",
    "Révolutionnaire": "revolutionnaire.png",
    "Sort du but": "sort-du-but.png",
    "Slide Tackle": "tacle-glisse.png",
    "Tacle glissé": "tacle-glisse.png",
    "Technicien": "technicien.png",
    "Technique": "technique.png",
    "Tête précise": "tete-precise.png",
    "Tiki-Taka": "tiki-taka.png",
    "Tir en finesse": "tir-en-finesse.png",
    "Tir puissant": "tir-puissant.png",
    "Tir rasant appuyé": "tir-rasant-appuye.png",
}

# Playstyles+ variants from archive
PLAYSTYLES_PLUS_IMAGES = {
    "Acrobatique+": "acrobatique-plus.png",
    "Ballon piqué+": "ballon-pique-plus.png",
    "Coups de pied arrêtés+": "coup-de-pied-arrete-plus.png",
    "Tête précise+": "tete-precise-plus.png",
    "Tir en finesse+": "tir-en-finesse-plus.png",
    "Tir puissant+": "tir-puissant-plus.png",
    "Tir rasant appuyé+": "tir-rasant-appuye-plus.png",
}

print("\n" + "="*90)
print("PLAYSTYLES IMAGES - COMPLETE MAPPING")
print("="*90 + "\n")

# Create correct CSV
csv_file = 'playstyles_images_mapping.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Type', 'Playstyle Name', 'Image Filename', 'Path', 'Status'])
    
    # Playstyles+ variants
    print("PLAYSTYLES+ (Variants with + suffix):")
    print("-" * 90)
    for name, filename in sorted(PLAYSTYLES_PLUS_IMAGES.items()):
        path = f'/assets/playstyles_plus/{filename}'
        full_path = f'archive_assets/ea_playstyles_plus_icons/{filename}'
        exists = os.path.exists(full_path)
        status = "✓ EXISTS" if exists else "✗ MISSING"
        writer.writerow(['playstyles+', name, filename, path, status])
        print(f"  {name:30s} → {filename:40s} {status}")
    
    print(f"\nTotal playstyles+: {len(PLAYSTYLES_PLUS_IMAGES)}\n")
    
    # Playstyles
    print("PLAYSTYLES (Base playstyles without +):")
    print("-" * 90)
    count = 0
    for name, filename in sorted(PLAYSTYLES_MAPPING.items()):
        if '+' not in name:  # Only base playstyles
            if filename:
                path = f'/assets/playstyles/{filename}'
                full_path = f'public/assets/playstyles/{filename}'
                exists = os.path.exists(full_path)
                status = "✓ EXISTS" if exists else "✗ MISSING"
                writer.writerow(['playstyles', name, filename, path, status])
                print(f"  {name:30s} → {filename:40s} {status}")
                count += 1
            else:
                writer.writerow(['playstyles', name, 'MISSING', '', '✗ NO IMAGE'])
                print(f"  {name:30s} → {'MISSING':40s} ✗ NO IMAGE")
                count += 1
    
    print(f"\nTotal playstyles: {count}\n")

print("="*90)
print("SUMMARY:")
print(f"  Playstyles+ images (with suffix): {len(PLAYSTYLES_PLUS_IMAGES)}")
print(f"  Playstyles images (base): {count}")
print(f"  Total images available: {len(PLAYSTYLES_PLUS_IMAGES) + count}")
print("="*90 + "\n")

print(f"✓ CSV generated: {csv_file}\n")
