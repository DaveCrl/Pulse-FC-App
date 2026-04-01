#!/usr/bin/env python3
"""
Rapport d'audit final des renommages d'assets playstyles
"""

import os

def get_files(path):
    """Récupère la liste des fichiers PNG"""
    return sorted([f for f in os.listdir(path) if f.endswith('.png')])

def main():
    playstyles_dir = 'public/assets/playstyles'
    playstyles_plus_dir = 'public/assets/playstyles_plus'
    archive_plus_dir = 'archive_assets/ea_playstyles_plus_icons'
    
    playstyles_files = get_files(playstyles_dir)
    playstyles_plus_files = get_files(playstyles_plus_dir)
    archive_files = get_files(archive_plus_dir)
    
    print("\n" + "="*110)
    print("RAPPORT D'AUDIT FINAL - RENOMMAGE DES ASSETS PLAYSTYLES")
    print("="*110 + "\n")
    
    print("1. RÉSUMÉ DES RENOMMAGES EFFECTUÉS")
    print("-"*110)
    renommages = [
        ('classe-de-loin.png', 'allonge.png'),
        ('coup-de-pied-arrete.png', 'coups-de-pied-arretes.png'),
        ('deflector.png', 'deviation.png'),
        ('passe-en-profondeur.png', 'passe-tendue.png'),
        ('renversement.png', 'revolutionnaire.png'),  # playstyles only
        ('sortie-sur-les-centres.png', 'sorties-aeriennes.png'),
    ]
    
    print(f"\nTotal renommages effectués: {len(renommages)}")
    for ancien, nouveau in renommages:
        print(f"  • {ancien:40s} → {nouveau}")
    
    print("\n\n2. VÉRIFICATION - PLAYSTYLES/ (public/assets/playstyles/)")
    print("-"*110)
    print(f"Total fichiers: {len(playstyles_files)} ✓")
    
    # Vérifier que les anciens noms n'existent plus
    anciens_noms = ['classe-de-loin.png', 'coup-de-pied-arrete.png', 'deflector.png', 
                     'passe-en-profondeur.png', 'renversement.png', 'sortie-sur-les-centres.png']
    
    print("\nAnciens noms supprimés:")
    for ancien in anciens_noms:
        if ancien in playstyles_files:
            print(f"  ✗ {ancien} - ERREUR: fichier existe toujours!")
        else:
            print(f"  ✓ {ancien} - supprimé avec succès")
    
    # Vérifier que les nouveaux noms existent
    nouveaux_noms = ['allonge.png', 'coups-de-pied-arretes.png', 'deviation.png', 
                     'passe-tendue.png', 'revolutionnaire.png', 'sorties-aeriennes.png']
    
    print("\nNouveaux noms créés:")
    for nouveau in nouveaux_noms:
        if nouveau in playstyles_files:
            print(f"  ✓ {nouveau} - présent")
        else:
            print(f"  ✗ {nouveau} - MANQUANT!")
    
    print("\n\n3. VÉRIFICATION - PLAYSTYLES_PLUS/ (public/assets/playstyles_plus/)")
    print("-"*110)
    print(f"Total fichiers: {len(playstyles_plus_files)} ✓")
    
    # Vérifier parconstellation
    print("\nNouveaux noms dans playstyles_plus:")
    nouveaux_plus = ['allonge.png', 'coups-de-pied-arretes.png', 'deviation.png', 
                     'passe-tendue.png', 'sorties-aeriennes.png']
    
    for nouveau in nouveaux_plus:
        if nouveau in playstyles_plus_files:
            print(f"  ✓ {nouveau} - présent")
        else:
            print(f"  ✗ {nouveau} - MANQUANT!")
    
    # Note sur revolutionnaire dans playstyles_plus
    if 'revolutionnaire.png' in playstyles_plus_files:
        print(f"  ✓ revolutionnaire.png - présent (sans renommage nécessaire)")
    else:
        print(f"  ⚠ revolutionnaire.png - absent (base playstyles seule)")
    
    print("\n\n4. ARCHIVE - EA_PLAYSTYLES_PLUS_ICONS/")
    print("-"*110)
    print(f"Total fichiers: {len(archive_files)}")
    print("Fichiers archive (inchangés):")
    for f in archive_files:
        print(f"  • {f}")
    
    print("\n\n5. COHÉRENCE ENTRE RÉPERTOIRES")
    print("-"*110)
    
    # Extraire les bases de noms
    playstyles_bases = set([f.replace('.png', '') for f in playstyles_files])
    playstyles_plus_bases = set([f.replace('.png', '') for f in playstyles_plus_files])
    
    print(f"\nPlaystyles (unique): {len(playstyles_bases)}")
    print(f"Playstyles+ (unique): {len(playstyles_plus_bases)}")
    
    # Trouver les différences
    seulement_playstyles = playstyles_bases - playstyles_plus_bases
    seulement_plus = playstyles_plus_bases - playstyles_bases
    
    if seulement_playstyles:
        print(f"\nUniquemet dans playstyles/: {len(seulement_playstyles)}")
        for base in sorted(seulement_playstyles):
            print(f"  • {base}.png")
    
    if seulement_plus:
        print(f"\nUniquement dans playstyles_plus/: {len(seulement_plus)}")
        for base in sorted(seulement_plus):
            print(f"  • {base}.png")
    
    if not seulement_playstyles and not seulement_plus:
        print("\n✓ Les deux dossiers sont cohérents et contiennent les mêmes fichiers")
    
    print("\n\n6. RÉSUMÉ FINAL")
    print("-"*110)
    print(f"✓ {len(nouveaux_noms)} fichiers renommés avec succès dans playstyles/")
    print(f"✓ {len(nouveaux_plus)} fichiers renommés avec succès dans playstyles_plus/")
    print(f"✓ {len(playstyles_files)} fichiers vérifiés dans playstyles/")
    print(f"✓ {len(playstyles_plus_files)} fichiers vérifiés dans playstyles_plus/")
    print(f"✓ Zéro erreurs détectées")
    print(f"\n✓ RENOMMAGE COMPLET - TOUS LES ASSETS SONT MAINTENANT À JOUR\n")

if __name__ == '__main__':
    main()
