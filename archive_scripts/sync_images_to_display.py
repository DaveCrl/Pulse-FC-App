#!/usr/bin/env python3
"""
Synchronise les clubs, ligues et nations avec leurs images pour le site
Crée les fichiers src/data appropriés avec tous les clubs/ligues/nations
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def get_available_images(image_dir):
    """Récupère les fichiers image disponibles dans un répertoire"""
    if not os.path.exists(image_dir):
        return set()
    return set(f.replace('.png', '') for f in os.listdir(image_dir) if f.endswith('.png'))

def slug_from_name(name):
    """Convertit un nom en slug"""
    return name.lower().replace(' ', '-').replace('_', '-')

def main():
    # ════════════════════════════════════════════════════════════════
    # 1. CLUBS
    # ════════════════════════════════════════════════════════════════
    print("🔍 Processing CLUBS...")
    
    with open('players_merged.json', 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    # Extraire tous les clubs uniques
    player_clubs = set()
    for player in players:
        if 'club' in player and player['club']:
            player_clubs.add(player['club'])
    
    print(f"  Found {len(player_clubs)} unique clubs in players")
    
    # Charger les images disponibles
    club_images = get_available_images('public/assets/clubs')
    print(f"  Found {len(club_images)} club images in public/assets/clubs/")
    
    # Créer les entrées pour les clubs
    clubs_data = []
    for club_name in sorted(player_clubs):
        club_slug = slug_from_name(club_name)
        
        # Chercher l'image (match exact ou proche)
        image_filename = None
        if club_slug in club_images:
            image_filename = club_slug
        else:
            # Chercher un match approximatif
            for img in club_images:
                if club_name.lower().replace(' ', '-') in img or img in club_name.lower().replace(' ', '-'):
                    image_filename = img
                    break
        
        club_entry = {
            'slug': club_slug,
            'nom': club_name,
            'name': club_name,
            'icon_filename': f'{image_filename}.png' if image_filename else 'default-club.png',
            'icon': f'/assets/clubs/{image_filename}.png' if image_filename else '/assets/clubs/default-club.png',
            'local_path': f'local_files/club_icons/{image_filename}.png' if image_filename else 'local_files/club_icons/default-club.png',
            'has_image': image_filename is not None
        }
        clubs_data.append(club_entry)
    
    # ════════════════════════════════════════════════════════════════
    # 2. LIGUES
    # ════════════════════════════════════════════════════════════════
    print("🔍 Processing LEAGUES...")
    
    # Extraire tous les ligues uniques
    player_leagues = set()
    for player in players:
        if 'ligue' in player and player['ligue']:
            player_leagues.add(player['ligue'])
    
    print(f"  Found {len(player_leagues)} unique leagues in players")
    
    # Charger les images disponibles
    league_images = get_available_images('public/assets/leagues')
    print(f"  Found {len(league_images)} league images in public/assets/leagues/")
    
    # Créer les entrées pour les ligues
    leagues_data = []
    for league_name in sorted(player_leagues):
        league_slug = slug_from_name(league_name)
        
        # Chercher l'image
        image_filename = None
        if league_slug in league_images:
            image_filename = league_slug
        else:
            # Chercher un match approximatif
            for img in league_images:
                if league_name.lower().replace(' ', '-') in img or img in league_name.lower().replace(' ', '-'):
                    image_filename = img
                    break
        
        league_entry = {
            'slug': league_slug,
            'nom': league_name,
            'name': league_name,
            'icon_filename': f'{image_filename}.png' if image_filename else 'default-league.png',
            'icon': f'/assets/leagues/{image_filename}.png' if image_filename else '/assets/leagues/default-league.png',
            'local_path': f'local_files/league_icons/{image_filename}.png' if image_filename else 'local_files/league_icons/default-league.png',
            'has_image': image_filename is not None
        }
        leagues_data.append(league_entry)
    
    # ════════════════════════════════════════════════════════════════
    # 3. NATIONS
    # ════════════════════════════════════════════════════════════════
    print("🔍 Processing NATIONS...")
    
    # Extraire tous les nationalités uniques
    player_nations = set()
    for player in players:
        if 'nationalite' in player and player['nationalite']:
            player_nations.add(player['nationalite'])
    
    print(f"  Found {len(player_nations)} unique nations in players")
    
    # Charger les nations.json original pour la structure
    with open('nations.json', 'r', encoding='utf-8') as f:
        original_nations = json.load(f)
    
    # Créer un mapping nom -> données originales
    nation_map = {n['name']: n for n in original_nations}
    
    # Créer les entrées pour les nations
    nations_data = []
    for nation_name in sorted(player_nations):
        nation_slug = slug_from_name(nation_name)
        
        # Chercher dans les données originales
        original = nation_map.get(nation_name)
        if original:
            nation_entry = {
                'slug': original.get('slug', nation_slug),
                'nom': nation_name,
                'name': nation_name,
                'url': original.get('url', ''),
            }
        else:
            nation_entry = {
                'slug': nation_slug,
                'nom': nation_name,
                'name': nation_name,
                'url': '',
            }
        nations_data.append(nation_entry)
    
    # ════════════════════════════════════════════════════════════════
    # SAUVEGARDE
    # ════════════════════════════════════════════════════════════════
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs('src/data', exist_ok=True)
    
    # Sauvegarder les fichiers
    with open('src/data/clubs.json', 'w', encoding='utf-8') as f:
        json.dump(clubs_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(clubs_data)} clubs to src/data/clubs.json")
    
    with open('src/data/leagues.json', 'w', encoding='utf-8') as f:
        json.dump(leagues_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(leagues_data)} leagues to src/data/leagues.json")
    
    with open('src/data/nations.json', 'w', encoding='utf-8') as f:
        json.dump(nations_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(nations_data)} nations to src/data/nations.json")
    
    # ════════════════════════════════════════════════════════════════
    # RAPPORT
    # ════════════════════════════════════════════════════════════════
    
    clubs_with_images = sum(1 for c in clubs_data if c['has_image'])
    leagues_with_images = sum(1 for c in leagues_data if c['has_image'])
    
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    print(f"Clubs: {len(clubs_data)} total, {clubs_with_images} avec image, {len(clubs_data) - clubs_with_images} sans image")
    print(f"Ligues: {len(leagues_data)} total, {leagues_with_images} avec image, {len(leagues_data) - leagues_with_images} sans image")
    print(f"Nations: {len(nations_data)} total")

if __name__ == '__main__':
    main()
