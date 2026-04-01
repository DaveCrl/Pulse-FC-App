#!/usr/bin/env python3
"""
Audit et plan de nettoyage des assets playstyles
"""

import os
import shutil

# Nomenclature validée (slug → pour les fichiers)
NOMENCLATURE_VALIDEE = {
    'acrobatique',
    'agressif',
    'allonge',
    'anticipation',
    'arret-du-pied',
    'ballon-pique',
    'contre',
    'controle',
    'coups-de-pied-arretes',
    'deviation',
    'fantaisiste',
    'forteresse-aerienne',
    'foulee-rapide',
    'infatigable',
    'interception',
    'longue-relance',
    'longue-touche',
    'lutte',
    'passage-en-force',
    'passe-incisive',
    'passe-longue',
    'passe-tendue',
    'passe-travaillee',
    'rapide',
    'resiste-au-pressing',
    'revolutionnaire',
    'sort-du-but',
    'sorties-aeriennes',
    'tacle-glisse',
    'technicien',
    'technique',
    'tete-precise',
    'tiki-taka',
    'tir-en-finesse',
    'tir-puissant',
    'tir-rasant-appuye',
}

# Corrections spéciales: ancien_nom → nouveau_nom
RENOMMAGES_NECESSAIRES = {
    'classe-de-loin.png': 'allonge.png',
    'deflector.png': 'deviation.png',
    'sortie-sur-les-centres.png': 'sorties-aeriennes.png',
    'coup-de-pied-arrete.png': 'coups-de-pied-arretes.png',
    'passe-en-profondeur.png': 'passe-tendue.png',
    'renversement.png': 'revolutionnaire.png',
}

# Playstyles+ variants
PLAYSTYLES_PLUS_ATTENDUS = {
    'acrobatique-plus.png',
    'ballon-pique-plus.png',
    'coups-de-pied-arretes-plus.png',  # Will be renamed
    'tete-precise-plus.png',
    'tir-en-finesse-plus.png',
    'tir-puissant-plus.png',
    'tir-rasant-appuye-plus.png',
}

def audit_dossier(chemin):
    """Audit un dossier d'assets"""
    files = sorted([f for f in os.listdir(chemin) if f.endswith('.png')])
    return files

def analyser_fichiers(files_actuels):
    """Analyse les fichiers et détermine les actions"""
    resultats = {
        'corrects': [],
        'a_renommer': [],
        'inconnus': [],
        'manquants': []
    }
    
    # Fichiers actuels (sans .png)
    fichiers_bases = set([f.replace('.png', '').replace('-plus', '') for f in files_actuels])
    
    # Vérifier chaque fichier
    for f in files_actuels:
        base = f.replace('.png', '')
        
        # Vérifier s'il y a un renommage nécessaire
        if f in RENOMMAGES_NECESSAIRES:
            resultats['a_renommer'].append((f, RENOMMAGES_NECESSAIRES[f]))
        # Vérifier si c'est dans la nomenclature
        elif base in NOMENCLATURE_VALIDEE or base.replace('-plus', '') in NOMENCLATURE_VALIDEE:
            resultats['corrects'].append(f)
        else:
            resultats['inconnus'].append(f)
    
    # Vérifier les manquants
    for slug in NOMENCLATURE_VALIDEE:
        expected = f'{slug}.png'
        if expected not in files_actuels and slug not in [f.replace('.png', '') for f in files_actuels]:
            # Vérifier si c'est pas un renommage
            found = False
            for ancien, nouveau in RENOMMAGES_NECESSAIRES.items():
                if nouveau == expected:
                    found = True
                    break
            if not found:
                resultats['manquants'].append(expected)
    
    return resultats

def main():
    print("\n" + "="*100)
    print("AUDIT ET PLAN DE NETTOYAGE DES ASSETS PLAYSTYLES")
    print("="*100 + "\n")
    
    playstyles_dir = 'public/assets/playstyles'
    playstyles_plus_dir = 'public/assets/playstyles_plus'
    archive_plus_dir = 'archive_assets/ea_playstyles_plus_icons'
    
    # Audit de chaque dossier
    print("1. PLAYSTYLES (base)")
    print("-" * 100)
    playstyles_files = audit_dossier(playstyles_dir)
    playstyles_analysis = analyser_fichiers(playstyles_files)
    
    print(f"   Total fichiers: {len(playstyles_files)}")
    print(f"   Fichiers corrects: {len(playstyles_analysis['corrects'])}")
    print(f"   À renommer: {len(playstyles_analysis['a_renommer'])}")
    print(f"   Inconnus: {len(playstyles_analysis['inconnus'])}")
    print(f"   Manquants: {len(playstyles_analysis['manquants'])}")
    
    if playstyles_analysis['a_renommer']:
        print("\n   Fichiers À RENOMMER:")
        for ancien, nouveau in playstyles_analysis['a_renommer']:
            print(f"     {ancien:40s} → {nouveau}")
    
    print("\n2. PLAYSTYLES+ (tous les variants)")
    print("-" * 100)
    plus_files = audit_dossier(playstyles_plus_dir)
    plus_analysis = analyser_fichiers(plus_files)
    
    print(f"   Total fichiers: {len(plus_files)}")
    print(f"   Fichiers corrects: {len(plus_analysis['corrects'])}")
    print(f"   À renommer: {len(plus_analysis['a_renommer'])}")
    print(f"   Inconnus: {len(plus_analysis['inconnus'])}")
    
    if plus_analysis['a_renommer']:
        print("\n   Fichiers À RENOMMER:")
        for ancien, nouveau in plus_analysis['a_renommer']:
            print(f"     {ancien:40s} → {nouveau}")
    
    print("\n3. ARCHIVE (playstyles+ originaux)")
    print("-" * 100)
    archive_files = audit_dossier(archive_plus_dir)
    print(f"   Total fichiers: {len(archive_files)}")
    for f in sorted(archive_files):
        print(f"     {f}")
    
    # Résumé des renommages
    print("\n" + "="*100)
    print("PLAN D'ACTION")
    print("="*100 + "\n")
    
    total_renommages = len(playstyles_analysis['a_renommer']) + len(plus_analysis['a_renommer'])
    print(f"Total renommages à effectuer: {total_renommages}\n")
    
    # Afficher le plan complet
    print("PLAYSTYLES (public/assets/playstyles/):")
    for ancien, nouveau in playstyles_analysis['a_renommer']:
        print(f"  mv '{ancien}' '{nouveau}'")
    
    print("\nPLAYSTYLES+ (public/assets/playstyles_plus/):")
    for ancien, nouveau in plus_analysis['a_renommer']:
        print(f"  mv '{ancien}' '{nouveau}'")
    
    # Plan de vérification
    print("\n" + "="*100)
    print("VÉRIFICATION POST-RENOMMAGE")
    print("="*100 + "\n")
    
    print("Attendus dans playstyles/: 35 fichiers")
    print("Attendus dans playstyles_plus/: 7 fichiers (.plus)\n")
    
    return {
        'playstyles': playstyles_analysis,
        'playstyles_plus': plus_analysis,
        'archive': archive_files
    }

if __name__ == '__main__':
    results = main()
