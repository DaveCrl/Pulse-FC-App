#!/usr/bin/env python3
"""
Audit and update playstyles from CSV reference
- Reads CSV playstyles
- Separates playstyles and playstyles_plus
- Updates players_clean.json using ID as key
- Generates detailed audit report
"""

import json
import csv
import ast
from collections import defaultdict
from typing import Dict, List, Tuple

def parse_csv_playstyles():
    """Parse CSV and extract playstyles by player ID"""
    csv_file = 'EAFC26 copy.csv'
    playstyles_by_id = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            player_id = int(row['ID'])
            player_name = row['Name']
            play_style_str = row['play style']
            
            # Parse the play style column (it's a JSON-like string)
            try:
                # The column contains a list representation like ['Finesse Shot+', 'First Touch', ...]
                play_styles_list = ast.literal_eval(play_style_str)
                if not isinstance(play_styles_list, list):
                    play_styles_list = []
            except (ValueError, SyntaxError):
                play_styles_list = []
            
            # Separate into playstyles and playstyles_plus
            playstyles = []
            playstyles_plus = []
            
            for ps in play_styles_list:
                if ps.endswith('+'):
                    playstyles_plus.append(ps)
                else:
                    playstyles.append(ps)
            
            playstyles_by_id[player_id] = {
                'name': player_name,
                'playstyles': playstyles,
                'playstyles_plus': playstyles_plus,
                'all_playstyles': play_styles_list
            }
    
    return playstyles_by_id


def update_players_json(playstyles_by_id: Dict) -> Tuple[int, int, int, List[int], int, int]:
    """
    Update players_clean.json with new playstyles
    Returns: (updated_count, found_by_id, not_found_by_id, not_found_ids, total_plus, total_normal)
    """
    json_file = 'src/data/players_clean.json'
    
    # Load current players
    with open(json_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    updated_count = 0
    not_found = []
    total_playstyles_plus = 0
    total_playstyles_normal = 0
    
    # Create a map for quick lookup
    csv_id_set = set(playstyles_by_id.keys())
    
    # Update each player
    for player in players:
        player_id = player.get('id')
        
        if player_id in playstyles_by_id:
            csv_data = playstyles_by_id[player_id]
            
            # Replace playstyles with the new values from CSV
            # Store both separated and combined for reference
            player['playstyles'] = csv_data['all_playstyles']
            player['playstyles_plus'] = csv_data['playstyles_plus']
            player['playstyles_normal'] = csv_data['playstyles']
            
            total_playstyles_plus += len(csv_data['playstyles_plus'])
            total_playstyles_normal += len(csv_data['playstyles'])
            updated_count += 1
        else:
           # This shouldn't happen since both files have 17873 players
            not_found.append(player_id)
    
    # Save updated players
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)
    
    found_by_id = len(playstyles_by_id)
    not_found_by_id = len(not_found)
    
    return updated_count, found_by_id, not_found_by_id, not_found, total_playstyles_plus, total_playstyles_normal


def generate_audit_report(
    updated_count: int,
    found_by_id: int,
    not_found_by_id: int,
    not_found_ids: List[int],
    total_playstyles_plus: int,
    total_playstyles_normal: int,
    playstyles_by_id: Dict
) -> str:
    """Generate a detailed audit report"""
    
    report = []
    report.append("=" * 80)
    report.append("FC PULSE - PLAYSTYLES AUDIT & UPDATE REPORT")
    report.append("=" * 80)
    report.append("")
    
    report.append("1. SUMMARY")
    report.append("-" * 80)
    report.append(f"   Files updated: 1 (src/data/players_clean.json)")
    report.append(f"   Total players updated: {updated_count}")
    report.append(f"   CSV players processed: {found_by_id}")
    report.append(f"   Players found by ID in JSON: {updated_count}")
    report.append(f"   Players NOT found by ID: {not_found_by_id}")
    report.append("")
    
    report.append("2. PLAYSTYLES STATISTICS")
    report.append("-" * 80)
    report.append(f"   Total playstyles+ extracted: {total_playstyles_plus}")
    report.append(f"   Total playstyles (normal) extracted: {total_playstyles_normal}")
    report.append(f"   Average playstyles+ per player: {total_playstyles_plus / updated_count:.2f}")
    report.append(f"   Average playstyles per player: {total_playstyles_normal / updated_count:.2f}")
    report.append("")
    
    if not_found_ids:
        report.append("3. NOT FOUND PLAYERS")
        report.append("-" * 80)
        report.append(f"   Count: {len(not_found_ids)}")
        for pid in not_found_ids[:10]:
            report.append(f"   - ID: {pid}")
        if len(not_found_ids) > 10:
            report.append(f"   ... and {len(not_found_ids) - 10} more")
        report.append("")
    
    # Sample data for verification
    report.append("4. SAMPLE DATA (First 5 players from CSV)")
    report.append("-" * 80)
    for i, (player_id, data) in enumerate(list(playstyles_by_id.items())[:5]):
        report.append(f"   Player ID: {player_id} ({data['name']})")
        report.append(f"     - All playstyles: {data['all_playstyles']}")
        report.append(f"     - Playstyles+: {data['playstyles_plus']}")
        report.append(f"     - Playstyles (normal): {data['playstyles']}")
        report.append("")
    
    report.append("5. DATA PRESERVATION")
    report.append("-" * 80)
    report.append("   Structure changes:")
    report.append("   - [{OLD}] players.playstyles = [translated French playstyles]")
    report.append("   - [{NEW}] players.playstyles = [English playstyles from CSV]")
    report.append("   - [{NEW}] players.playstyles_plus = [English playstyles+ from CSV]")
    report.append("   - [{NEW}] players.playstyles_normal = [English playstyles (no +) from CSV]")
    report.append("")
    
    report.append("6. NEXT STEPS (NOT DONE YET)")
    report.append("-" * 80)
    report.append("   - TODO: Translation mapping (playstyles EN -> FR)")
    report.append("   - TODO: Image mapping (playstyles -> icon paths)")
    report.append("   - TODO: UI component updates if needed")
    report.append("")
    
    report.append("=" * 80)
    report.append("STATUS: ✓ PLAYSTYLES REPLACEMENT COMPLETE")
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    print("Starting FC Pulse playstyles audit and update...")
    print()
    
    # Step 1: Parse CSV
    print("Step 1/3: Parsing CSV playstyles...")
    playstyles_by_id = parse_csv_playstyles()
    print(f"  ✓ Extracted {len(playstyles_by_id)} players from CSV")
    print()
    
    # Step 2: Update JSON
    print("Step 2/3: Updating players_clean.json...")
    updated_count, found_by_id, not_found_by_id, not_found_ids, total_plus, total_normal = \
        update_players_json(playstyles_by_id)
    print(f"  ✓ Updated {updated_count} players")
    print(f"  ✓ Found by ID: {found_by_id}")
    print(f"  ✓ Not found: {not_found_by_id}")
    print(f"  ✓ Total playstyles+: {total_plus}")
    print(f"  ✓ Total playstyles: {total_normal}")
    print()
    
    # Step 3: Generate report
    print("Step 3/3: Generating audit report...")
    report = generate_audit_report(
        updated_count, found_by_id, not_found_by_id, not_found_ids,
        total_plus, total_normal, playstyles_by_id
    )
    
    # Save and display report
    with open('AUDIT_REPORT_PLAYSTYLES.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print()
    print(f"✓ Report saved to: AUDIT_REPORT_PLAYSTYLES.txt")


if __name__ == '__main__':
    main()
