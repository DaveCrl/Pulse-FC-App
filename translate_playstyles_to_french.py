#!/usr/bin/env python3
"""
Renaming playstyles from English to French based on validated mapping table
"""

import json
import copy
from typing import Dict, List, Tuple

# VALIDATED MAPPING TABLE (SOURCE OF TRUTH)
PLAYSTYLE_MAPPING = {
    "Acrobatic": "Acrobatique",
    "Aerial Fortress": "Forteresse aérienne",
    "Anticipate": "Anticipation",
    "Block": "Contre",
    "Bruiser": "Agressif",
    "Chip Shot": "Ballon piqué",
    "Cross Claimer": "Sorties aériennes",
    "Dead Ball": "Coups de pied arrêtés",
    "Deflector": "Déviation",
    "Enforcer": "Passage en force",
    "Far Reach": "Allonge",
    "Far Throw": "Longue relance",
    "Finesse Shot": "Tir en finesse",
    "First Touch": "Contrôle",
    "Footwork": "Arrêt du pied",
    "Gamechanger": "Révolutionnaire",
    "Incisive Pass": "Passe incisive",
    "Intercept": "Interception",
    "Inventive": "Fantaisiste",
    "Jockey": "Lutte",
    "Long Ball Pass": "Passe longue",
    "Long Throw": "Longue touche",
    "Low Driven Shot": "Tir rasant appuyé",
    "Pinged Pass": "Passe tendue",
    "Power Shot": "Tir puissant",
    "Precision Header": "Tête précise",
    "Press Proven": "Résiste au pressing",
    "Quick Step": "Foulée rapide",
    "Rapid": "Rapide",
    "Relentless": "Infatigable",
    "Rush Out": "Sort du but",
    "Slide Tackle": "Tacle glissé",
    "Technical": "Technique",
    "Tiki Taka": "Tiki-Taka",
    "Trickster": "Technicien",
    "Whipped Pass": "Passe travaillée",
}


def translate_playstyle(playstyle: str) -> Tuple[str, bool]:
    """
    Translate a playstyle using the mapping table.
    Returns: (translated_name, is_plus) where is_plus indicates if it had a '+' suffix
    """
    is_plus = playstyle.endswith('+')
    base_name = playstyle.rstrip('+')
    
    if base_name in PLAYSTYLE_MAPPING:
        translated = PLAYSTYLE_MAPPING[base_name]
        if is_plus:
            translated += '+'
        return translated, True
    
    return playstyle, False


def audit_playstyles(players_file: str) -> Tuple[Dict, List]:
    """
    Audit all playstyles in the file to identify any missing from mapping
    """
    with open(players_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    all_playstyles = set()
    unmapped = set()
    
    for player in players:
        for ps in player.get('playstyles_plus', []):
            base = ps.rstrip('+')
            all_playstyles.add(base)
            if base not in PLAYSTYLE_MAPPING:
                unmapped.add(ps)
        
        for ps in player.get('playstyles_normal', []):
            all_playstyles.add(ps)
            if ps not in PLAYSTYLE_MAPPING:
                unmapped.add(ps)
    
    return {"total": len(all_playstyles), "found": all_playstyles}, list(unmapped)


def apply_translation(players_file: str) -> Tuple[int, int, int, List]:
    """
    Apply translation to all playstyles in players file
    Returns: (playstyles_translated, playstyles_plus_translated, players_updated, unmapped_items)
    """
    with open(players_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    playstyles_count = 0
    playstyles_plus_count = 0
    unmapped_items = []
    
    for player in players:
        # Translate playstyles_plus
        if 'playstyles_plus' in player:
            new_plus = []
            for ps in player['playstyles_plus']:
                translated, found = translate_playstyle(ps)
                new_plus.append(translated)
                if found:
                    playstyles_plus_count += 1
                else:
                    unmapped_items.append((player['id'], player.get('nom', 'Unknown'), ps))
            player['playstyles_plus'] = new_plus
        
        # Translate playstyles_normal
        if 'playstyles_normal' in player:
            new_normal = []
            for ps in player['playstyles_normal']:
                translated, found = translate_playstyle(ps)
                new_normal.append(translated)
                if found:
                    playstyles_count += 1
                else:
                    unmapped_items.append((player['id'], player.get('nom', 'Unknown'), ps))
            player['playstyles_normal'] = new_normal
        
        # Translate main playstyles array
        if 'playstyles' in player:
            new_playstyles = []
            for ps in player['playstyles']:
                translated, found = translate_playstyle(ps)
                new_playstyles.append(translated)
            player['playstyles'] = new_playstyles
    
    # Save updated file
    with open(players_file, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)
    
    players_updated = len(players)
    return playstyles_count, playstyles_plus_count, players_updated, unmapped_items


def verify_translation(players_file: str) -> Dict:
    """
    Verify that translation was applied correctly
    """
    with open(players_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    results = {
        "total_players": len(players),
        "players_with_playstyles": 0,
        "players_with_playstyles_plus": 0,
        "total_playstyles": 0,
        "total_playstyles_plus": 0,
        "french_playstyles": set(),
        "french_playstyles_plus": set(),
        "issues": []
    }
    
    for player in players:
        if player.get('playstyles_normal'):
            results["players_with_playstyles"] += 1
            for ps in player['playstyles_normal']:
                results["total_playstyles"] += 1
                results["french_playstyles"].add(ps)
                # Check for English names
                if ps in PLAYSTYLE_MAPPING.values():
                    pass  # It's in French
                elif ps in PLAYSTYLE_MAPPING:
                    results["issues"].append(f"Found English playstyle: {ps} (Player {player['id']})")
        
        if player.get('playstyles_plus'):
            results["players_with_playstyles_plus"] += 1
            for ps in player['playstyles_plus']:
                results["total_playstyles_plus"] += 1
                base = ps.rstrip('+')
                results["french_playstyles_plus"].add(ps)
    
    results["french_playstyles"] = sorted(list(results["french_playstyles"]))
    results["french_playstyles_plus"] = sorted(list(results["french_playstyles_plus"]))
    
    return results


def main():
    players_file = 'src/data/players_clean.json'
    
    print("=" * 80)
    print("FC PULSE - PLAYSTYLES TRANSLATION TO FRENCH")
    print("=" * 80)
    print()
    
    # Step 1: Audit
    print("Step 1/4: Auditing playstyles...")
    audit_result, unmapped = audit_playstyles(players_file)
    print(f"  ✓ Total unique playstyles found: {audit_result['total']}")
    if unmapped:
        print(f"  ⚠ Unmapped playstyles detected: {len(unmapped)}")
        for item in unmapped:
            print(f"    - {item}")
    print()
    
    # Step 2: Apply translation
    print("Step 2/4: Applying translation...")
    ps_count, ps_plus_count, players_count, unmapped_during = apply_translation(players_file)
    print(f"  ✓ Playstyles translated: {ps_count}")
    print(f"  ✓ Playstyles+ translated: {ps_plus_count}")
    print(f"  ✓ Players updated: {players_count}")
    if unmapped_during:
        print(f"  ⚠ Unmapped during translation: {len(unmapped_during)}")
    print()
    
    # Step 3: Verify
    print("Step 3/4: Verifying translation...")
    verify_result = verify_translation(players_file)
    print(f"  ✓ Total players: {verify_result['total_players']}")
    print(f"  ✓ Players with playstyles: {verify_result['players_with_playstyles']}")
    print(f"  ✓ Players with playstyles+: {verify_result['players_with_playstyles_plus']}")
    print(f"  ✓ Total playstyles used: {verify_result['total_playstyles']}")
    print(f"  ✓ Total playstyles+ used: {verify_result['total_playstyles_plus']}")
    print()
    
    if verify_result['issues']:
        print(f"  ⚠ Issues found: {len(verify_result['issues'])}")
        for issue in verify_result['issues'][:5]:
            print(f"    - {issue}")
    else:
        print(f"  ✓ No issues detected (all translated to French)")
    print()
    
    # Step 4: Sample verification
    print("Step 4/4: Sample verification...")
    with open(players_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
        sample_player = next((p for p in players if p['id'] == 209331), None)
        if sample_player:
            print(f"  Sample player: {sample_player['nom']} (ID: 209331)")
            print(f"    - playstyles_plus: {sample_player.get('playstyles_plus', [])}")
            print(f"    - playstyles_normal (first 3): {sample_player.get('playstyles_normal', [])[:3]}")
    print()
    
    print("=" * 80)
    print("✓ TRANSLATION COMPLETE")
    print("=" * 80)
    
    return {
        "playstyles_translated": ps_count,
        "playstyles_plus_translated": ps_plus_count,
        "players_updated": players_count,
        "unmapped": unmapped_during,
        "verification": verify_result
    }


if __name__ == '__main__':
    results = main()
