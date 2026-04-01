import json

# Verify the updated JSON structure
with open('src/data/players_clean.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

print("✓ Verification of Updated Structure")
print("=" * 80)
print()

# Check 5 sample players
sample_ids = [209331, 231747, 241667, 237288, 246219]
sample_players = {p['id']: p for p in players if p['id'] in sample_ids}

for player_id in sample_ids:
    if player_id in sample_players:
        p = sample_players[player_id]
        print(f"Player: {p.get('nom', 'N/A')} (ID: {player_id})")
        print(f"  playstyles field: {p.get('playstyles', [])}")
        print(f"  playstyles_plus field: {p.get('playstyles_plus', [])}")
        print(f"  playstyles_normal field: {p.get('playstyles_normal', [])}")
        print()

# Count players with playstyles_plus
players_with_plus = sum(1 for p in players if len(p.get('playstyles_plus', [])) > 0)
print("=" * 80)
print(f"Players with playstyles+: {players_with_plus}")
print(f"Players without playstyles+: {len(players) - players_with_plus}")
print(f"Total players: {len(players)}")
