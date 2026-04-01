#!/usr/bin/env python3
"""
Extract all unique playstyles and create a CSV file
"""
import json
import csv

# Load the updated players file
with open('src/data/players_clean.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

# Extract all unique playstyles
playstyles_set = set()
playstyles_plus_set = set()

for player in players:
    for ps in player.get('playstyles_normal', []):
        playstyles_set.add(ps)
    for ps in player.get('playstyles_plus', []):
        playstyles_plus_set.add(ps)

# Sort them
playstyles_sorted = sorted(list(playstyles_set))
playstyles_plus_sorted = sorted(list(playstyles_plus_set))

print(f"Total unique playstyles: {len(playstyles_sorted)}")
print(f"Total unique playstyles+: {len(playstyles_plus_sorted)}")

# Create CSV file
csv_file = 'playstyles_complete_list.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Header
    writer.writerow(['Type', 'Playstyle Name', 'Count Players'])
    
    # Write playstyles+
    for ps_plus in playstyles_plus_sorted:
        count = sum(1 for p in players if ps_plus in p.get('playstyles_plus', []))
        writer.writerow(['playstyles+', ps_plus, count])
    
    # Write playstyles (normal)
    for ps_normal in playstyles_sorted:
        count = sum(1 for p in players if ps_normal in p.get('playstyles_normal', []))
        writer.writerow(['playstyles', ps_normal, count])

print(f"\n✓ CSV file created: {csv_file}")
print(f"  Total entries: {len(playstyles_plus_sorted) + len(playstyles_sorted)}")
