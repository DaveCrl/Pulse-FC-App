#!/usr/bin/env python3
"""
Génère la table de mapping centrale des playstyles
Source: Table de référence validée
Output: public/data/reference/playstyles-map.json
"""

import json
import os
from pathlib import Path

# TABLE DE RÉFÉRENCE VALIDÉE
PLAYSTYLES_REFERENCE = [
    ("Acrobatic", "Acrobatique", "acrobatique"),
    ("Aerial Fortress", "Forteresse aérienne", "forteresse-aerienne"),
    ("Anticipate", "Anticipation", "anticipation"),
    ("Block", "Contre", "contre"),
    ("Bruiser", "Agressif", "agressif"),
    ("Chip Shot", "Ballon piqué", "ballon-pique"),
    ("Cross Claimer", "Sorties aériennes", "sorties-aeriennes"),
    ("Dead Ball", "Coups de pied arrêtés", "coups-de-pied-arretes"),
    ("Deflector", "Déviation", "deviation"),
    ("Enforcer", "Passage en force", "passage-en-force"),
    ("Far Reach", "Allonge", "allonge"),
    ("Far Throw", "Longue relance", "longue-relance"),
    ("Finesse Shot", "Tir en finesse", "tir-en-finesse"),
    ("First Touch", "Contrôle", "controle"),
    ("Footwork", "Arrêt du pied", "arret-du-pied"),
    ("Gamechanger", "Révolutionnaire", "revolutionnaire"),
    ("Incisive Pass", "Passe incisive", "passe-incisive"),
    ("Intercept", "Interception", "interception"),
    ("Inventive", "Fantaisiste", "fantaisiste"),
    ("Jockey", "Lutte", "lutte"),
    ("Long Ball Pass", "Passe longue", "passe-longue"),
    ("Long Throw", "Longue touche", "longue-touche"),
    ("Low Driven Shot", "Tir rasant appuyé", "tir-rasant-appuye"),
    ("Pinged Pass", "Passe tendue", "passe-tendue"),
    ("Power Shot", "Tir puissant", "tir-puissant"),
    ("Precision Header", "Tête précise", "tete-precise"),
    ("Press Proven", "Résiste au pressing", "resiste-au-pressing"),
    ("Quick Step", "Foulée rapide", "foulee-rapide"),
    ("Rapid", "Rapide", "rapide"),
    ("Relentless", "Infatigable", "infatigable"),
    ("Rush Out", "Sort du but", "sort-du-but"),
    ("Slide Tackle", "Tacle glissé", "tacle-glisse"),
    ("Technical", "Technique", "technique"),
    ("Tiki Taka", "Tiki-Taka", "tiki-taka"),
    ("Trickster", "Technicien", "technicien"),
    ("Whipped Pass", "Passe travaillée", "passe-travaillee"),
]

def check_asset_exists(slug, is_plus=False):
    """Vérifie si un asset existe"""
    folder = "playstyles_plus" if is_plus else "playstyles"
    path = f"public/assets/{folder}/{slug}.png"
    return os.path.exists(path)

def generate_playstyles_map():
    """Génère la table de mapping complète"""
    
    print("\n" + "="*120)
    print("GÉNÉRATION DE LA TABLE DE MAPPING CENTRALE - PLAYSTYLES")
    print("="*120 + "\n")
    
    # Résultats
    mapping_data = []
    assets_found = 0
    assets_missing = 0
    missing_list = []
    
    print("Traitement des 36 playstyles...\n")
    
    for key_en, label_fr, slug in PLAYSTYLES_REFERENCE:
        # Vérifier les assets
        asset_exists = check_asset_exists(slug, is_plus=False)
        asset_plus_exists = check_asset_exists(slug, is_plus=True)
        
        # Construire l'objet
        entry = {
            "key": key_en,
            "label_fr": label_fr,
            "slug": slug,
            "asset": f"/assets/playstyles/{slug}.png" if asset_exists else None,
            "asset_plus": f"/assets/playstyles_plus/{slug}.png" if asset_plus_exists else None,
            "asset_exists": asset_exists,
            "asset_plus_exists": asset_plus_exists,
        }
        
        # Comptage
        if asset_exists:
            assets_found += 1
        else:
            assets_missing += 1
            missing_list.append((slug, "playstyles"))
        
        if asset_plus_exists:
            assets_found += 1
        else:
            assets_missing += 1
            missing_list.append((slug, "playstyles_plus"))
        
        # Status
        status = "✓" if (asset_exists and asset_plus_exists) else "⚠"
        print(f"{status} {key_en:25s} → {label_fr:30s} ({slug})")
        if not asset_exists:
            print(f"  ⚠ Manquant: playstyles/{slug}.png")
        if not asset_plus_exists:
            print(f"  ⚠ Manquant: playstyles_plus/{slug}.png")
        
        mapping_data.append(entry)
    
    # Créer le dossier destination
    output_dir = "public/data/reference"
    os.makedirs(output_dir, exist_ok=True)
    
    # Écrire le fichier JSON
    output_file = os.path.join(output_dir, "playstyles-map.json")
    
    # Version "produit" (sans les flags de vérification)
    mapping_clean = []
    for entry in mapping_data:
        clean_entry = {
            "key": entry["key"],
            "label_fr": entry["label_fr"],
            "slug": entry["slug"],
        }
        if entry["asset"]:
            clean_entry["asset"] = entry["asset"]
        if entry["asset_plus"]:
            clean_entry["asset_plus"] = entry["asset_plus"]
        mapping_clean.append(clean_entry)
    
    # Écrire le fichier
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping_clean, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*120)
    print("RAPPORT D'AUDIT")
    print("="*120 + "\n")
    
    print(f"Total playstyles mappés: {len(mapping_data)}/36")
    print(f"Assets trouvés: {assets_found}/72")  # 36 base + 36 plus
    print(f"Assets manquants: {len(missing_list)}")
    
    if missing_list:
        print("\nAssets manquants:")
        for slug, folder in sorted(set(missing_list)):
            print(f"  ✗ {folder}/{slug}.png")
    
    print(f"\n✓ Fichier généré: {output_file}")
    print(f"  Taille: {len(json.dumps(mapping_clean))} bytes")
    print(f"  Entrées: {len(mapping_clean)}")
    
    # Vérifier la cohérence
    print("\n" + "-"*120)
    print("VÉRIFICATION DE COHÉRENCE")
    print("-"*120 + "\n")
    
    # Tous les slugs uniques
    all_slugs = set([entry["slug"] for entry in mapping_data])
    print(f"Slugs uniques: {len(all_slugs)}")
    
    # Vérifier les doublons
    slug_list = [entry["slug"] for entry in mapping_data]
    if len(slug_list) == len(set(slug_list)):
        print("✓ Pas de doublons dans les slugs")
    else:
        print("✗ ERREUR: Doublons détectés!")
    
    # Vérifier les clés anglaises uniques
    keys = [entry["key"] for entry in mapping_data]
    if len(keys) == len(set(keys)):
        print("✓ Toutes les clés anglaises sont uniques")
    else:
        print("✗ ERREUR: Doublons dans les clés!")
    
    # Vérifier les labels français
    labels = [entry["label_fr"] for entry in mapping_data]
    if len(labels) == len(set(labels)):
        print("✓ Tous les labels français sont uniques")
    else:
        print("✗ ERREUR: Doublons dans les labels!")
    
    print("\n" + "="*120)
    print("✓ GÉNÉRATION TERMINÉE")
    print("="*120 + "\n")
    
    return {
        "total": len(mapping_data),
        "assets_found": assets_found,
        "assets_missing": len(missing_list),
        "missing_details": missing_list,
        "output_file": output_file
    }

if __name__ == '__main__':
    results = generate_playstyles_map()
