import os
import json
import logging
import time
from typing import List, Dict, Any

from playwright.sync_api import sync_playwright, Page, TimeoutError

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

INDEX_JSON = os.path.join(DATA_DIR, "campaigns_index.json")
OUT_PLAYERS_JSON = os.path.join(DATA_DIR, "campaign_players.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

# Filtre strict exigé par la donnée métier
REGULAR_TYPES = [
    "gold",
    "rare gold",
    "common gold",
    "silver",
    "rare silver",
    "common silver",
    "bronze",
    "rare bronze",
    "common bronze"
]

def is_regular_card(card_type: str) -> bool:
    """Vérifie le type de carte pour notre filtre Anti-Regular."""
    if not card_type:
        return False
    return card_type.lower().strip() in REGULAR_TYPES

# ==========================================
# SCRAPING LOGIC
# ==========================================
def extract_players_from_squad(page: Page, campaign: Dict[str, Any]) -> List[Dict[str, Any]]:
    players = []
    
    # 🎯 Ajustement du Sélecteur :
    # Sur FUTBIN, les grilles de joueurs de squad sont généralement
    # des div avec une structure cartographique contenant une balise "a".
    # Il faudra sans doute ajuster ce bloc après exécution manuelle sur FUT FC 26.
    player_cards = page.locator('a[href*="/player/"]')
    
    count = player_cards.count()
    logging.info(f"   -> Vérification de {count} liens joueurs bruts sur la page.")
    
    seen_urls = set()
    
    for i in range(count):
        card = player_cards.nth(i)
        
        url_href = card.get_attribute("href")
        if not url_href: continue
        
        player_url = f"https://www.futbin.com{url_href}" if url_href.startswith("/") else url_href
        if player_url in seen_urls:
            continue
        seen_urls.add(player_url)
        
        # ⚠️ EXTRACTIONS METIERS (Adaptées à la structure table-row de FUTBIN 26)
        # Nom de Joueur
        name_loc = card.locator('.leader-name, .name, .pcdisplay-name')
        player_name = name_loc.inner_text().strip() if name_loc.count() > 0 else "Unknown Player"
        
        # Tentative depuis le noeud texte lui-même si pas de balise span/div spécifique
        if player_name == "Unknown Player":
            txt = card.inner_text().strip()
            if txt and len(txt) > 2:
                # Les sauts de lignes ou espaces inutiles
                player_name = txt.replace('\\n', '').strip()
                
        if player_name == "Unknown Player":
            continue
                
        # Note, Position
        rating = 0
        position = "N/A"
        
        # On remonte au parent <tr> ou <li> pour chercher les colonnes sœurs
        row = card.locator('xpath=ancestor::tr | ancestor::div[contains(@class, "table-row")]').first
        if row.count() > 0:
            tds = row.locator('td, .td')
            # Souvent : [0: Player link, 1: Position, 2: Rating, 3: Prix...]
            if tds.count() >= 3:
                pos_text = tds.nth(1).inner_text().strip()
                rat_text = tds.nth(2).inner_text().strip()
                if pos_text: position = pos_text
                if rat_text.isdigit(): rating = int(rat_text)
                
        # Fallback si ce n'est pas une table (layout grid cartographique classique)
        if rating == 0:
            rating_loc = card.locator('.pcdisplay-rat, .rating')
            if rating_loc.count() > 0:
                try: rating = int(rating_loc.inner_text().strip())
                except ValueError: pass
        if position == "N/A":
            pos_loc = card.locator('.pcdisplay-pos, .position')
            position = pos_loc.inner_text().strip() if pos_loc.count() > 0 else "N/A"
        
        # Type de carte (Rarity/Version)
        # Si manquant visuellement, on suppose par défaut qu'il appartient à cette promotion. 
        # (Sauf mention Gold/Silver/Bronze trouvée ailleurs dans le DOM de la carte).
        card_type_loc = card.locator('.card-type, .rarity')
        if card_type_loc.count() > 0:
            card_type = card_type_loc.inner_text().strip()
        else:
            card_type = campaign["name"]
            
        # Si la div, la carte ou l'image mentionne par hasard "gold" en classes, on affine le type.
        # Attention : FUTBIN utilise parfois le sprite "3_gold.png" ou "totw_gold" pour certains backgrounds,
        # donc l'heuristique doit être prudente. Ici on le laisse tel quel (validera la promo par défaut).
                
        # Image
        img_loc = card.locator('img.player-img, img.pcdisplay-picture, img')
        card_image = img_loc.first.get_attribute("src") if img_loc.count() > 0 else "N/A"

        # Nationalité / Ligue / Club :
        # FUTBIN masque très souvent des mini drapeaux ou logos. L'enrichissement ultérieur
        # via FUT.GG (Phase C) sera souvent nécessaire pour blinder ces attributs proprement.
        club = "Unknown"
        league = "Unknown" 
        nation = "Unknown"
        
        # 🚫 FILTRE ANTI-REGULAR EXÉCUTÉ ICI
        if is_regular_card(card_type):
            logging.info(f"   -> 🚫 {player_name} ignoré (Carte Regular détectée: {card_type})")
            continue
            
        players.append({
            "campaign_slug": campaign["slug"],
            "campaign_name": campaign["name"],
            "date": campaign["date"],
            "player_name": player_name,
            "rating": rating,
            "position": position,
            "club": club,
            "league": league,
            "nation": nation,
            "card_type": card_type,
            "is_regular": False,  # Puisqu'on a passé le filtre avec succès
            "player_url": player_url,
            "card_image": card_image
        })
        
    return players

def main():
    if not os.path.exists(INDEX_JSON):
        logging.error(f"Fichier manquant : {INDEX_JSON}. Lancez 'scrape_campaigns_index.py' d'abord !")
        return
        
    with open(INDEX_JSON, "r", encoding="utf-8") as f:
        campaigns = json.load(f)
        
    if not campaigns:
        logging.error("L'index des campagnes est vide.")
        return
        
    logging.info(f"🚀 Début Phase B : Traitement de {len(campaigns)} campagnes trouvées...")
    
    all_players = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 🛡️ Protection basique contre le blocage automatisé de FUTBIN / Cloudflare
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        try:
            for idx, campaign in enumerate(campaigns, 1):
                url = campaign.get("url")
                if not url:
                    continue
                    
                logging.info(f"\n[{idx}/{len(campaigns)}] Visite de la campagne : {campaign['name']}")
                
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    
                    # Pause pour valider la génération asynchrone des composants de FUTBIN
                    page.wait_for_timeout(2000) 
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                    page.wait_for_timeout(1000)
                    
                    extracted = extract_players_from_squad(page, campaign)
                    all_players.extend(extracted)
                    
                    logging.info(f"   -> ✅ Validés : {len(extracted)} joueurs retenus depuis {campaign['name']}.")
                    
                except TimeoutError:
                    logging.warning(f"   -> ❌ Timeout impossible à franchir sur {campaign['name']}. Ignorée temporairement.")
                    
                # Rate limit artificiel pour contourner IP BAN
                time.sleep(1.5)
                
        finally:
            browser.close()

    logging.info("\n--- STATISTIQUES FINALES ---")
    if not all_players:
        logging.warning("⚠️ Aucun joueur final exporté ! Vos sélecteurs Playwright `.locator()` nécessitent une mise à jour d'après le layout strict de l'URL utilisée par FC 26 FUTBIN.")
        return
        
    # Export du JSON massif avec filtre réussi
    with open(OUT_PLAYERS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_players, f, indent=2, ensure_ascii=False)
        
    logging.info(f"🎉 Scraping Phase B terminé avec un immense succès !")
    logging.info(f"📊 {len(all_players)} joueurs sauvegardés dans {OUT_PLAYERS_JSON}")

if __name__ == "__main__":
    main()
