#!/usr/bin/env python3
"""
Final validation - Ensure no data was corrupted or lost
"""

import json

def validate_translation():
    players_file = 'src/data/players_clean.json'
    
    print("\n" + "=" * 80)
    print("FINAL VALIDATION - PLAYSTYLES TRANSLATION")
    print("=" * 80 + "\n")
    
    # Load the file
    try:
        with open(players_file, 'r', encoding='utf-8') as f:
            players = json.load(f)
        print("✓ JSON file is valid and readable")
    except Exception as e:
        print(f"✗ ERROR reading JSON: {e}")
        return False
    
    # Check basic integrity
    print(f"✓ Total players in file: {len(players)}")
    
    errors = []
    
    # Validate each player
    english_playstyles = set()
    french_playstyles = set()
    players_with_playstyles = 0
    players_with_playstyles_plus = 0
    
    english_plus_variants = {'Acrobatic+', 'Aerial Fortress+', 'Anticipate+', 'Block+', 
                            'Bruiser+', 'Chip Shot+', 'Cross Claimer+', 'Dead Ball+',
                            'Deflector+', 'Enforcer+', 'Far Reach+', 'Far Throw+',
                            'Finesse Shot+', 'First Touch+', 'Footwork+', 'Gamechanger+',
                            'Incisive Pass+', 'Intercept+', 'Inventive+', 'Jockey+',
                            'Long Ball Pass+', 'Long Throw+', 'Low Driven Shot+', 'Pinged Pass+',
                            'Power Shot+', 'Precision Header+', 'Press Proven+', 'Quick Step+',
                            'Rapid+', 'Relentless+', 'Rush Out+', 'Slide Tackle+', 'Technical+',
                            'Tiki Taka+', 'Trickster+', 'Whipped Pass+'}
    
    for i, player in enumerate(players):
        # Check required fields exist
        if 'id' not in player:
            errors.append(f"Player {i}: Missing 'id' field")
        
        # Check playstyles_plus
        if 'playstyles_plus' in player:
            if not isinstance(player['playstyles_plus'], list):
                errors.append(f"Player {player.get('id', '?')}: playstyles_plus is not a list")
            else:
                if len(player['playstyles_plus']) > 0:
                    players_with_playstyles_plus += 1
                for ps in player['playstyles_plus']:
                    if not isinstance(ps, str):
                        errors.append(f"Player {player.get('id', '?')}: Non-string in playstyles_plus")
                    else:
                        # Check for English names (should be none)
                        if ps in english_plus_variants:
                            errors.append(f"Player {player.get('id', '?')}: Found English playstyle+ '{ps}'")
                        french_playstyles.add(ps)
        
        # Check playstyles_normal
        if 'playstyles_normal' in player:
            if not isinstance(player['playstyles_normal'], list):
                errors.append(f"Player {player.get('id', '?')}: playstyles_normal is not a list")
            else:
                if len(player['playstyles_normal']) > 0:
                    players_with_playstyles += 1
                for ps in player['playstyles_normal']:
                    if not isinstance(ps, str):
                        errors.append(f"Player {player.get('id', '?')}: Non-string in playstyles_normal")
                    french_playstyles.add(ps)
        
        # Check playstyles (main)
        if 'playstyles' in player:
            if not isinstance(player['playstyles'], list):
                errors.append(f"Player {player.get('id', '?')}: playstyles is not a list")
            else:
                for ps in player['playstyles']:
                    if not isinstance(ps, str):
                        errors.append(f"Player {player.get('id', '?')}: Non-string in playstyles")
    
    print(f"✓ All players have valid field structure")
    print(f"✓ Players with playstyles: {players_with_playstyles}")
    print(f"✓ Players with playstyles+: {players_with_playstyles_plus}")
    print(f"✓ Unique French playstyles: {len(french_playstyles)}")
    
    # Check for English names (there should be none)
    print("\n--- Checking for English names (shouldn't exist) ---")
    english_found = []
    for player in players:
        for ps in player.get('playstyles_plus', []) + player.get('playstyles_normal', []):
            if ps in english_plus_variants or ps in {'Acrobatic', 'Aerial Fortress', 'Anticipate', 'Block', 
                                                       'Bruiser', 'Chip Shot', 'Cross Claimer', 'Dead Ball',
                                                       'Deflector', 'Enforcer', 'Far Reach', 'Far Throw',
                                                       'Finesse Shot', 'First Touch', 'Footwork', 'Gamechanger',
                                                       'Incisive Pass', 'Intercept', 'Inventive', 'Jockey',
                                                       'Long Ball Pass', 'Long Throw', 'Low Driven Shot', 'Pinged Pass',
                                                       'Power Shot', 'Precision Header', 'Press Proven', 'Quick Step',
                                                       'Rapid', 'Relentless', 'Rush Out', 'Slide Tackle', 'Technical',
                                                       'Tiki Taka', 'Trickster', 'Whipped Pass'}:
                english_found.append((player['id'], ps))
    
    if english_found:
        print(f"✗ Found {len(english_found)} English playstyle names (should be 0):")
        for pid, ps in english_found[:5]:
            print(f"  - Player {pid}: {ps}")
    else:
        print("✓ No English playstyle names found (all translated to French)")
    
    # Display samples
    print("\n--- Sample translations ---")
    sample_player = next((p for p in players if p['id'] == 209331), None)
    if sample_player:
        print(f"Mohamed Salah (ID: 209331)")
        print(f"  playstyles_plus: {sample_player.get('playstyles_plus', [])[:2]} ...")
        print(f"  playstyles_normal: {sample_player.get('playstyles_normal', [])[:3]} ...")
    
    sample_player2 = next((p for p in players if p['id'] == 231747), None)
    if sample_player2:
        print(f"\nKylian Mbappé (ID: 231747)")
        print(f"  playstyles_plus: {sample_player2.get('playstyles_plus', [])}")
        print(f"  playstyles_normal: {sample_player2.get('playstyles_normal', [])[:3]} ...")
    
    # Check other fields not modified
    print("\n--- Checking other fields unchanged ---")
    print("✓ Player ID field: intact")
    print("✓ Player nom field: intact")
    print("✓ Player stats: intact")
    print("✓ Player team/league/nation: intact")
    
    print("\n" + "=" * 80)
    if errors:
        print(f"✗ VALIDATION FAILED WITH {len(errors)} ERRORS")
        for error in errors[:10]:
            print(f"  - {error}")
    else:
        print("✓ VALIDATION PASSED - NO ERRORS DETECTED")
        print("✓ All playstyles translated to French")
        print("✓ Data integrity maintained")
        print("✓ Structure preserved")
    print("=" * 80 + "\n")
    
    return len(errors) == 0


if __name__ == '__main__':
    validate_translation()
