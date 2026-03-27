import os
import json
import logging

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

INDEX_JSON = os.path.join(DATA_DIR, "campaigns_index.json")
PLAYERS_JSON = os.path.join(DATA_DIR, "campaign_players.json")
OUT_FULL_JSON = os.path.join(DATA_DIR, "campaigns_full.json")

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s | %(levelname)s | %(message)s", 
    datefmt="%H:%M:%S"
)

def main():
    if not os.path.exists(INDEX_JSON) or not os.path.exists(PLAYERS_JSON):
        logging.error("❌ Fichiers sources manquants. Exécutez d'abord les scripts de scrapping (A et B).")
        return

    # 1. Charger l'index des campagnes
    with open(INDEX_JSON, "r", encoding="utf-8") as f:
        campaigns_index = json.load(f)

    # 2. Charger tous les joueurs
    with open(PLAYERS_JSON, "r", encoding="utf-8") as f:
        players = json.load(f)

    logging.info(f"🚀 Lancement Phase C (Optionnelle): Regroupement de {len(players)} joueurs dans {len(campaigns_index)} campagnes.")

    # 3. Créer le dictionnaire de mapping basé sur les slugs uniques
    campaigns_map = {}
    for c in campaigns_index:
        campaigns_map[c["slug"]] = {
            "slug": c["slug"],
            "name": c["name"],
            "date": c["date"],
            "players": []
        }

    # 4. Peupler les joueurs
    match_count = 0
    orphan_count = 0

    for p in players:
        c_slug = p.get("campaign_slug")
        
        if c_slug and c_slug in campaigns_map:
            # On clone le dictionnaire pour nettoyer les clés redondantes
            player_clean = p.copy()
            
            # Plus besoin de ces clés puisqu'on est physiquement dans l'objet Campagne
            player_clean.pop("campaign_slug", None)
            player_clean.pop("campaign_name", None)
            player_clean.pop("date", None)
            
            campaigns_map[c_slug]["players"].append(player_clean)
            match_count += 1
        else:
            orphan_count += 1

    # 5. Formater la sortie finale : une liste contenant les campagnes peuplées
    output_data = {
        "campaigns": list(campaigns_map.values())
    }

    # 6. Sauvegarde
    with open(OUT_FULL_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    logging.info(f"✅ Transformation réussie avec brio !")
    logging.info(f"📊 Campagnes structurées : {len(campaigns_map)}")
    logging.info(f"👤 Joueurs insérés : {match_count}")
    
    if orphan_count > 0:
        logging.warning(f"⚠️ {orphan_count} joueurs orphelins ignorés (le `campaign_slug` ne matche pas avec l'Index).")
        
    logging.info(f"📁 Fichier Maître généré : {OUT_FULL_JSON}")

if __name__ == "__main__":
    main()
