#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

with open('/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/src/data/players_clean.json', encoding='utf-8') as f:
    players = json.load(f)

all_playstyles = set()
for p in players:
    if p.get('playstyles'):
        for ps in p['playstyles']:
            all_playstyles.add(ps)

print("Playstyles contenant 'tir':")
for ps in sorted(all_playstyles):
    if 'tir' in ps.lower():
        print(f"  - {ps}")

print("\nPlaystyles contenant 'pas':")
for ps in sorted(all_playstyles):
    if 'pas' in ps.lower():
        print(f"  - {ps}")

print("\nTous les playstyles uniques:")
for ps in sorted(all_playstyles):
    print(f"  - {ps}")
