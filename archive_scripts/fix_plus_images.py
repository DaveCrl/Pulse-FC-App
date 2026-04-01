#!/usr/bin/env python3
import json

# Mapping for + variants that need separate images
plus_variants_mapping = {
    'Contrôle+': 'controle',
    'Contrôle': 'controle',
    'Disponible+': 'disponible',
    'Rapide+': 'rapide',  # This should use rapide.png, NOT foulee-rapide.png
    'Foulée rapide+': 'rapide',  # Foulée rapide+ should map to rapide image
}

# Generate all + variant mappings
all_plus_mappings = {
    'Acrobatique+': 'acrobatique',
    'Agressif+': 'agressif',
    'Anticipation+': 'anticipation',
    'Arrêt de loin+': 'classe-de-loin',
    'Arrêts du pied+': 'arret-du-pied',
    'Ballon piqué+': 'ballon-pique',
    'Contrôle+': 'controle',
    'Contre+': 'contre',
    'Coup de pied arrêté+': 'coup-de-pied-arrete',
    'Décisif+': 'decisif',
    'Déviation+': 'deflector',
    'Forteresse aérienne+': 'forteresse-aerienne',
    'Foulée rapide+': 'rapide',  # KEY FIX: use rapide.png not foulee-rapide.png
    'Infatigable+': 'infatigable',
    'Interception+': 'interception',
    'Longue relance+': 'longue-relance',
    'Lutte+': 'lutte',
    'Passage en force+': 'passage-en-force',
    'Passe fusante+': 'passe-en-profondeur',
    'Passe incisive+': 'passe-incisive',
    'Passe longue+': 'passe-longue',
    'Passe travaillée +': 'passe-travaillee',
    'Résiste au pressing+': 'resiste-au-pressing',
    'Renversement+': 'renversement',
    'Sort du but+': 'sort-du-but',
    'Sortie sur les centres+': 'sortie-sur-les-centres',
    'Tacle glissé+': 'tacle-glisse',
    'Technicien+': 'technicien',
    'Technique+': 'technique',
    'Tête précise+': 'tete-precise',
    'Tir en finesse +': 'tir-en-finesse',
    'Tir puissant+': 'tir-puissant',
    'Tir rasant appuyé+': 'tir-rasant-appuye',
    'Tiki-taka+': 'tiki-taka',
}

filename = '/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_merged.json'

print("Loading...")
with open(filename, 'r', encoding='utf-8') as f:
    players = json.load(f)

print("Updating custom mappings will be handled in index.html")
print("\nVerifying player playstyles are correct...")

# Just verify status
correct = 0
issues = 0
for p in players:
    if p.get('nom') in ['Alexia Putellas', 'Aitana Bonmatí', 'Ousmane Dembélé']:
        ps = p.get('playstyles', [])
        has_tech = 'Technicien' in ps or 'Technicien+' in ps
        if has_tech:
            correct += 1
        else:
            issues += 1
            print(f"  ⚠ {p.get('nom')}: missing Technicien - has {ps}")

print(f"\n✓ Players verified: {correct}")
print(f"✗ Issues found: {issues}")
