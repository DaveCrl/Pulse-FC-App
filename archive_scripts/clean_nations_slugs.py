#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nettoyage des slugs nations
URL-decode les slugs et crée des versions propres
"""

import json
import urllib.parse

input_file = "nations.json"
output_file = "nations.json"

with open(input_file, 'r', encoding='utf-8') as f:
    nations = json.load(f)

print(f"Nettoyage de {len(nations)} nations...")

for nation in nations:
    # URL-decode le slug
    slug = nation.get('slug', '')
    clean_slug = urllib.parse.unquote(slug).lower()
    # Remplacer les espaces par des tirets
    clean_slug = clean_slug.replace(' ', '-')
    # Enlever les caractères spéciaux sauf les tirets
    clean_slug = ''.join(c if c.isalnum() or c == '-' else '' for c in clean_slug)
    
    nation['slug'] = clean_slug

# Sauvegarder
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(nations, f, ensure_ascii=False, indent=2)

print(f"✅ {len(nations)} nations nettoyées et sauvegardées dans {output_file}")

# Afficher les premiers pour vérification
print("\n📋 Échantillon après nettoyage:")
for nation in nations[:10]:
    print(f"  - {nation['name']:30} → {nation['slug']}")
