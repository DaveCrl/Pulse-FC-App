#!/usr/bin/env python3
"""
Script de validation - Vérifier que la table de mapping peut être utilisée
"""

import json
import os

def validate_mapping():
    """Valide la table de mapping pour utilisation production"""
    
    print("\n" + "="*120)
    print("VALIDATION - TABLE DE MAPPING PRÊTE POUR UTILISATION")
    print("="*120 + "\n")
    
    # Charger le mapping
    mapping_path = 'public/data/reference/playstyles-map.json'
    
    if not os.path.exists(mapping_path):
        print(f"✗ ERREUR: Fichier {mapping_path} non trouvé!")
        return False
    
    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    
    print(f"✓ Fichier chargé: {mapping_path}")
    print(f"  Taille: {os.path.getsize(mapping_path)} bytes")
    print(f"  Entrées: {len(mapping)}\n")
    
    # Vérifications de base
    print("TESTS DE VALIDITÉ")
    print("-"*120)
    
    issues = []
    
    # Test 1: Type et longueur
    if not isinstance(mapping, list):
        issues.append("✗ Le mapping doit être une liste")
    elif len(mapping) != 36:
        issues.append(f"✗ Attendu 36 entrées, trouvé {len(mapping)}")
    else:
        print("✓ Format: Array de 36 objets")
    
    # Test 2: Chaque entrée
    required_fields = {'key', 'label_fr', 'slug', 'asset', 'asset_plus'}
    for i, entry in enumerate(mapping):
        if not isinstance(entry, dict):
            issues.append(f"✗ Entrée {i} n'est pas un objet")
            continue
        
        missing = required_fields - set(entry.keys())
        if missing:
            issues.append(f"✗ Entrée {i} ({entry.get('key', 'UNKNOWN')}): champs manquants: {missing}")
        
        # Vérifier que les assets pointent vers les fichiers
        # Les chemins commencent par "/" donc on ajoute "public" au début
        asset_path = 'public' + entry.get('asset', '')
        asset_plus_path = 'public' + entry.get('asset_plus', '')
        
        if asset_path and not os.path.exists(asset_path):
            issues.append(f"✗ Asset manquant pour {entry.get('key')}: {asset_path}")
        
        if asset_plus_path and not os.path.exists(asset_plus_path):
            issues.append(f"✗ Asset+ manquant pour {entry.get('key')}: {asset_plus_path}")
    
    if not issues:
        print("✓ Toutes les entrées sont valides")
        print("✓ Tous les champs requis présents")
        print("✓ Tous les assets trouvés\n")
    else:
        print("\n".join(issues))
        print()
    
    # Test 3: Unicité
    print("TESTS D'UNICITÉ")
    print("-"*120)
    
    keys = [m['key'] for m in mapping]
    labels = [m['label_fr'] for m in mapping]
    slugs = [m['slug'] for m in mapping]
    
    print(f"✓ Clés uniques: {len(set(keys)) == len(keys)}")
    print(f"✓ Labels uniques: {len(set(labels)) == len(labels)}")
    print(f"✓ Slugs uniques: {len(set(slugs)) == len(slugs)}\n")
    
    # Test 4: Cohérence
    print("TESTS DE COHÉRENCE")
    print("-"*120)
    
    # Tous les assets base doivent exister
    base_assets = [m['asset'] for m in mapping]
    base_missing = [a for a in base_assets if not os.path.exists('public' + a)]
    if base_missing:
        print(f"✗ {len(base_missing)} assets base manquants")
    else:
        print(f"✓ Tous les 36 assets base trouvés")
    
    # Tous les assets+ doivent exister
    plus_assets = [m['asset_plus'] for m in mapping]
    plus_missing = [a for a in plus_assets if not os.path.exists('public' + a)]
    if plus_missing:
        print(f"✗ {len(plus_missing)} assets+ manquants")
    else:
        print(f"✓ Tous les 36 assets+ trouvés")
    
    print()
    
    # Test 5: Utilisation (exemple)
    print("CAS D'USAGE - EXEMPLE D'ACCÈS")
    print("-"*120)
    
    sample = mapping[0]
    print(f"""
    // Charger la table
    const playstyles = await fetch('public/data/reference/playstyles-map.json')
      .then(r => r.json())
    
    // Accéder à un playstyle
    const item = playstyles[0]
    console.log(item.key)           // "{sample['key']}"
    console.log(item.label_fr)      // "{sample['label_fr']}"
    console.log(item.slug)          // "{sample['slug']}"
    console.log(item.asset)         // "{sample['asset']}"
    console.log(item.asset_plus)    // "{sample['asset_plus']}"
    
    // Créer un index pour recherche rapide
    const bySlug = Object.fromEntries(playstyles.map(p => [p.slug, p]))
    console.log(bySlug['acrobatique'].label_fr)  // "Acrobatique"
    
    // Afficher l'asset dans l'UI
    <img src={{item.asset}} alt={{item.label_fr}} />
    """)
    
    print("="*120)
    if not issues and not base_missing and not plus_missing:
        print("✓✓✓ TABLE DE MAPPING COMPLÈTEMENT VALIDÉE ✓✓✓")
        print("="*120 + "\n")
        print("La table est prête pour utilisation en production.")
        print("Elle peut être consommée par:")
        print("  - Composants React (import ou fetch)")
        print("  - API/Backend")
        print("  - Scripts de validation")
        print("  - Utilitaires de mapping données\n")
        return True
    else:
        print("✗ DES PROBLÈMES DÉTECTÉS")
        print("="*120 + "\n")
        return False

if __name__ == '__main__':
    success = validate_mapping()
    exit(0 if success else 1)
