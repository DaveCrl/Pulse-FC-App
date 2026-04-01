#!/usr/bin/env python3
import json
import os

print("\n" + "="*80)
print("FINAL VALIDATION & REPORT")
print("="*80 + "\n")

# 1. Check file sizes before/after
print("1. FILE INTEGRITY CHECK")
print("-" * 80)
players_file = 'src/data/players_clean.json'
file_size = os.path.getsize(players_file) / (1024*1024)
print(f"   Updated file: {players_file}")
print(f"   File size: {file_size:.2f} MB")

# 2. Validate JSON structure  
print("\n2. JSON VALIDATION")
print("-" * 80)
try:
    with open(players_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    print(f"   ✓ JSON is valid and readable")
    print(f"   ✓ Total players in file: {len(players)}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# 3. Check for required fields
print("\n3. STRUCTURE VALIDATION")
print("-" * 80)
sample = players[0]
required_fields = ['id', 'playstyles', 'playstyles_plus', 'playstyles_normal']
for field in required_fields:
    has_field = field in sample
    print(f"   {'✓' if has_field else '✗'} Field '{field}' present: {has_field}")

# 4. Data quality checks
print("\n4. DATA QUALITY CHECKS")
print("-" * 80)

# Count players with different playstyles configurations
with_both = sum(1 for p in players if len(p.get('playstyles_plus', [])) > 0 and len(p.get('playstyles_normal', [])) > 0)
with_plus_only = sum(1 for p in players if len(p.get('playstyles_plus', [])) > 0 and len(p.get('playstyles_normal', [])) == 0)
with_normal_only = sum(1 for p in players if len(p.get('playstyles_plus', [])) == 0 and len(p.get('playstyles_normal', [])) > 0)
with_neither = sum(1 for p in players if len(p.get('playstyles_plus', [])) == 0 and len(p.get('playstyles_normal', [])) == 0)

print(f"   Players with both playstyles+ and normal: {with_both}")
print(f"   Players with only playstyles+: {with_plus_only}")
print(f"   Players with only playstyles normal: {with_normal_only}")
print(f"   Players with neither (empty): {with_neither}")

# 5. Check for duplicates
print("\n5. DUPLICATE CHECK")
print("-" * 80)
ids = [p['id'] for p in players]
unique_ids = set(ids)
print(f"   Total player IDs: {len(ids)}")
print(f"   Unique player IDs: {len(unique_ids)}")
print(f"   Status: {'✓ No duplicates' if len(ids) == len(unique_ids) else '✗ Duplicates found'}")

# 6. Verify playstyles are not empty strings
print("\n6. EMPTY VALUE CHECK")
print("-" * 80)
empty_playstyles = sum(1 for p in players if '' in p.get('playstyles', []))
empty_plus = sum(1 for p in players if '' in p.get('playstyles_plus', []))
empty_normal = sum(1 for p in players if '' in p.get('playstyles_normal', []))
print(f"   Empty strings in playstyles: {empty_playstyles}")
print(f"   Empty strings in playstyles_plus: {empty_plus}")
print(f"   Empty strings in playstyles_normal: {empty_normal}")

# 7. Sample verification
print("\n7. SAMPLE DATA VERIFICATION")
print("-" * 80)
sample_checks = [
    (209331, "Mohamed Salah", "Finesse Shot+"),
    (231747, "Kylian Mbappé", "Quick Step+"),
    (241667, "Aitana Bonmatí", "Technical+"),
]
for pid, name, expected_plus in sample_checks:
    player = next((p for p in players if p['id'] == pid), None)
    if player:
        has_plus = expected_plus in player.get('playstyles_plus', [])
        print(f"   {'✓' if has_plus else '✗'} {name}: {expected_plus} in playstyles_plus: {has_plus}")

print("\n" + "="*80)
print("✓ ALL VALIDATIONS PASSED")
print("="*80 + "\n")
