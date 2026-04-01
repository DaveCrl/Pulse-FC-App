#!/usr/bin/env python3
import json

with open('/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_merged.json', 'r', encoding='utf-8') as f:
    players = json.load(f)

# Find Putellas and Bonmati
for p in players:
    nom = p.get('nom', '')
    if 'Putellas' in nom or 'Bonmati' in nom or 'Dembelé' in nom or 'Mbappé' in nom:
        print(f"\n{'='*60}")
        print(f"Player: {nom}")
        print(f"{'='*60}")
        print(f"Playstyles: {p.get('playstyles', [])}")
        
        # Check for issues
        ps_list = p.get('playstyles', [])
        for ps in ps_list:
            if ps.endswith('+'):
                ps_base = ps.rstrip('+').strip()
                print(f"  ⚠ Found '+' variant: '{ps}' (base: '{ps_base}')")
