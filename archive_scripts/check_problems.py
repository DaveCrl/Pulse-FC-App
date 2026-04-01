#!/usr/bin/env python3
import json
from collections import Counter

with open('/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_merged.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

# Collect all playstyles
all_ps = []
for p in players:
    if 'playstyles' in p:
        all_ps.extend(p['playstyles'])

# Count
ps_count = Counter(all_ps)

# Show problematic ones
problem_terms = ['Pas Rapide', 'Pas rapide', 'Feinteur', 'Feinteur+', 'Passe Précise', 'Passe précise', 'Controle+', 'Inventif']

print("Searching for problematic playstyles:\n")
for term in problem_terms:
    count = ps_count.get(term, 0)
    if count > 0:
        print(f"❌ '{term}' appears {count} times")

# Also show what we do have for these categories
print("\n\nVariants of 'Rapide':")
for ps in sorted(ps_count.keys()):
    if 'rapide' in ps.lower():
        print(f"  ✓ '{ps}' = {ps_count[ps]}")

print("\nVariants of 'Feint/Tech':")
for ps in sorted(ps_count.keys()):
    if 'feint' in ps.lower() or 'technic' in ps.lower():
        print(f"  ✓ '{ps}' = {ps_count[ps]}")

print("\nVariants of 'Passe Précise/Fusante':")
for ps in sorted(ps_count.keys()):
    if ('précise' in ps.lower() or 'fusante' in ps.lower()) and 'passe' in ps.lower():
        print(f"  ✓ '{ps}' = {ps_count[ps]}")

print("\nVariants of 'Controle':")
for ps in sorted(ps_count.keys()):
    if 'contrôle' in ps.lower() or 'controle' in ps.lower():
        print(f"  ✓ '{ps}' = {ps_count[ps]}")

print("\nAll playstyles with '+' variant:")
for ps in sorted(ps_count.keys()):
    if '+' in ps:
        print(f"  '{ps}' = {ps_count[ps]}")
