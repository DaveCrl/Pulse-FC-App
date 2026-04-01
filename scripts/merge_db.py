import json
import re
import os

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def main():
    print("Chargement des données existantes...")
    with open('players_clean.json', 'r', encoding='utf-8') as f:
        base_players = json.load(f)

    print("Chargement des joueurs de campagne...")
    with open('data/campaign_players.json', 'r', encoding='utf-8') as f:
        campaign_players = json.load(f)

    # Création d'un dictionnaire des joueurs de base par slug/nom
    base_dict = {}
    for p in base_players:
        # Assurez-vous d'avoir une structure claire pour grouper
        slug = p.get('slug')
        if not slug:
           slug = slugify(p['nom'])
           p['slug'] = slug
        p['version_name'] = p.get('rarete', 'Regular')
        p['group_id'] = slug
        
        # S'il y a des doublons de "nom" dans base_players avec différentes notes
        # on prend la meilleure note ou on garde tous
        if slug not in base_dict:
            base_dict[slug] = []
        base_dict[slug].append(p)
    
    # Intégration des joueurs de campagne
    merged_list = list(base_players)
    
    for cp in campaign_players:
        name = cp.get('player_name', '')
        slug = slugify(name)
        
        # Chercher une correspondance dans base_players
        base_p = None
        if slug in base_dict:
            # S'il y a plusieurs versions de base, on prend la 1ère ou celle qui matche le mieux
            base_p = base_dict[slug][0]
        else:
            # Recherche partielle si slug ne correspond pas exactement
            # (pour Vinícius José de Oliveira Júnior vs Vini Jr.)
            for b_slug, b_list in base_dict.items():
                if name.lower() in b_slug or b_slug in name.lower():
                    base_p = b_list[0]
                    slug = b_slug
                    break
        
        new_player = {
            "id": f"campaign_{cp.get('campaign_slug')}_{slug}",
            "slug": slug,
            "group_id": slug,
            "nom": name if not base_p else base_p['nom'],
            "version_name": cp.get('campaign_name', 'Special'),
            "note": cp.get('rating'),
            "poste": cp.get('position'),
            "poste_fr": base_p['poste_fr'] if base_p else cp.get('position'),
            "club": cp.get('club') if cp.get('club') != "Unknown" else (base_p['club'] if base_p else "N/A"),
            "ligue": cp.get('league') if cp.get('league') != "Unknown" else (base_p['ligue'] if base_p else "N/A"),
            "nationalite": cp.get('nation') if cp.get('nation') != "Unknown" else (base_p['nationalite'] if base_p else "N/A"),
            "rarete": cp.get('campaign_name', 'Special'),
            "image_carte": cp.get('card_image'),
            "image_visage": base_p['image_visage'] if base_p else "",
            "stats": {"vitesse": "N/A", "tir": "N/A", "passes": "N/A", "dribble": "N/A", "defense": "N/A", "physique": "N/A"},
            "stats_detail": {},
            "meta": base_p['meta'] if base_p else {},
            "playstyles": base_p['playstyles'] if base_p else [],
            "campaign_url": cp.get('player_url', '')
        }
        
        # Update search_index
        new_player['search_index'] = f"{new_player['nom']} {new_player['club']} {new_player['ligue']} {new_player['nationalite']}".lower()

        merged_list.append(new_player)
    
    print(f"Fusion terminée ! Nombre de joueurs: {len(merged_list)}")
    
    # Sauvegarde du nouveau fichier
    with open('players_merged.json', 'w', encoding='utf-8') as f:
        json.dump(merged_list, f, ensure_ascii=False)
    print("Sauvegardé dans players_merged.json")

if __name__ == "__main__":
    main()
