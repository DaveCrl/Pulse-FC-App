"""
FC Pulse — Scraper FUT.GG
Récupère SBC, Objectifs et Évolutions actifs en temps réel
Output : sbcs.json, objectifs.json, evolutions.json

Usage :
    pip3 install requests beautifulsoup4
    python3 futgg_scraper.py

Respecte un délai entre les requêtes pour ne pas surcharger FUT.GG.
"""

import requests
import json
import time
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup

BASE        = "https://www.fut.gg"
DELAY       = 1.5   # secondes entre chaque requête
HEADERS     = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.fut.gg/",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# ──────────────────────────────────────────────────────────
# UTILITAIRES
# ──────────────────────────────────────────────────────────

def get(url, retries=3):
    """Requête GET avec retry automatique."""
    for attempt in range(retries):
        try:
            r = SESSION.get(url, timeout=15)
            r.raise_for_status()
            time.sleep(DELAY)
            return BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            print(f"  ⚠ Tentative {attempt+1}/{retries} échouée pour {url}: {e}")
            time.sleep(DELAY * 2)
    print(f"  ❌ Impossible de récupérer : {url}")
    return None

def clean(text):
    """Nettoie le texte HTML."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def extract_links(soup, pattern):
    """Extrait tous les liens correspondant à un pattern."""
    if not soup:
        return []
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.search(pattern, href):
            full = href if href.startswith("http") else BASE + href
            if full not in links:
                links.append(full)
    return links

def extract_expiry(soup):
    """Cherche une date d'expiration dans la page."""
    if not soup:
        return None
    text = soup.get_text()
    # Patterns : "Expires in X days", "Submit by in X days"
    patterns = [
        r'Expir(?:y|es?)[^\n]*?in\s+(\d+)\s+day',
        r'Submit by[^\n]*?in\s+(\d+)\s+day',
        r'Expires\s+(\w+\s+\w+)',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return None

def generate_id(url):
    """Génère un ID stable depuis l'URL."""
    slug = url.rstrip("/").split("/")[-1]
    return slug

def now_iso():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# ──────────────────────────────────────────────────────────
# NORMALISATION DES DONNÉES
# ──────────────────────────────────────────────────────────

DIFFICULTE_MAP = {
    "EasyNumber": "Facile",
    "Easy Number": "Facile",
    "MediumNumber": "Moyen",
    "Medium Number": "Moyen",
    "HardNumber": "Difficile",
    "Hard Number": "Difficile",
    "VeryHardNumber": "Très difficile",
    "Very Hard Number": "Très difficile",
    "ExpertNumber": "Expert",
    "Expert Number": "Expert",
    "Easy": "Facile",
    "Medium": "Moyen",
    "Hard": "Difficile",
    "Very Hard": "Très difficile",
}

RECOMPENSES_CLEAN = {
    "Small Gold Players Pack": "Pack joueurs or petit",
    "Gold Players Pack": "Pack joueurs or",
    "Rare Gold Players Pack": "Pack joueurs or rare",
    "Premium Gold Players Pack": "Pack joueurs or premium",
    "Electrum Players Pack": "Pack joueurs Electrum",
    "Prime Electrum Players Pack": "Pack joueurs Electrum Prime",
    "Gold Pack": "Pack or",
    "Rare Gold Pack": "Pack or rare",
    "Premium Gold Pack": "Pack or premium",
    "Players Pack": "Pack joueurs",
    "Player Pick": "Choix joueur",
    "Season Points": "Points de saison",
    "Evo Unlock": "Déverrouillage Évolution",
}

def normaliser_difficulte(raw):
    """Normalise la difficulté communautaire vers une valeur FR lisible."""
    if not raw:
        return ""
    for key, val in DIFFICULTE_MAP.items():
        if key.lower() in raw.lower():
            return val
    return raw.strip()

def normaliser_recompense(raw):
    """Normalise un nom de récompense."""
    if not raw:
        return raw
    for key, val in RECOMPENSES_CLEAN.items():
        if key in raw:
            return val
    return raw.strip()

def normaliser_conditions(conditions_brutes):
    """
    Nettoie et sépare les conditions d'éligibilité concaténées.
    Exemple : "Max. OVR: 80Max OVR: 88Max PS: 10" → liste propre
    """
    if not conditions_brutes:
        return []
    propres = []
    separateurs = re.compile(
        r'(?=Max\.|Min\.|Excluded|Required|Only|Position|Rarity|Nationality|League|Club)'
    )
    for cond in conditions_brutes:
        parties = [p.strip() for p in separateurs.split(cond) if p.strip()]
        for partie in parties:
            # Supprimer les redondances
            partie = re.sub(r'\s+', ' ', partie).strip()
            # Supprimer les entrées trop longues ou trop courtes
            if 3 < len(partie) < 80 and partie not in propres:
                propres.append(partie)
    return propres[:8]

def normaliser_expiry(texte):
    """Normalise le texte d'expiration en format FR lisible."""
    if not texte:
        return None
    # "Expiry in 5 days" → "Expire dans 5 jours"
    m = re.search(r'expir\w*[^\d]*(\d+)\s+day', texte, re.IGNORECASE)
    if m:
        d = int(m.group(1))
        return f"Expire dans {d} jour{'s' if d > 1 else ''}"
    # "Submit by in 3 days" → "Soumettre dans 3 jours"
    m = re.search(r'submit[^\d]*(\d+)\s+day', texte, re.IGNORECASE)
    if m:
        d = int(m.group(1))
        return f"Soumettre dans {d} jour{'s' if d > 1 else ''}"
    # "X hours"
    m = re.search(r'(\d+)\s+hour', texte, re.IGNORECASE)
    if m:
        h = int(m.group(1))
        return f"Expire dans {h}h"
    return texte

def deduplicar_recompenses(recompenses):
    """Déduplique et nettoie une liste de récompenses."""
    vues = set()
    propres = []
    for r in recompenses:
        r_clean = normaliser_recompense(r)
        key = r_clean.lower()
        if key not in vues and r_clean:
            vues.add(key)
            propres.append(r_clean)
    return propres

# ──────────────────────────────────────────────────────────
# SCRAPER SBC
# ──────────────────────────────────────────────────────────

def scrape_sbc_detail(url):
    """Scrape une page de détail SBC."""
    print(f"  → SBC: {url.split('/')[-2]}")
    soup = get(url)
    if not soup:
        return None

    title_el = soup.find("h1")
    titre = clean(title_el.get_text()) if title_el else ""
    # Nettoyer "- EA SPORTS FC 26 SBC" du titre
    titre = re.sub(r'\s*-\s*EA SPORTS FC 26.*', '', titre).strip()

    # Description
    desc = ""
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        t = clean(p.get_text())
        if len(t) > 30 and "FUT.GG" not in t:
            desc = t
            break

    # Récompense principale
    recompense = ""
    recompenses = []
    for img in soup.find_all("img", alt=True):
        alt = img.get("alt", "")
        if "Pack" in alt or "Player" in alt or "Pick" in alt:
            recompenses.append(alt)
    if recompenses:
        recompense = recompenses[0]

    # Segments / challenges
    segments = []
    # Chercher les sections h4 comme "PSG", "Portugal" etc.
    challenge_headers = soup.find_all("h4")
    for h in challenge_headers:
        seg_nom = clean(h.get_text())
        if not seg_nom or len(seg_nom) > 50:
            continue
        # Chercher les contraintes dans le bloc suivant
        contraintes = []
        note_requise = 0
        next_el = h.find_next_sibling()
        # Chercher les li/ul dans les éléments suivants
        parent = h.parent
        if parent:
            items = parent.find_all("li")
            for li in items:
                txt = clean(li.get_text())
                if txt:
                    m = re.search(r'Team Rating.*?(\d+)', txt)
                    if m:
                        note_requise = int(m.group(1))
                    elif txt:
                        contraintes.append(txt)

        segments.append({
            "nom": seg_nom,
            "note_requise": note_requise,
            "contraintes": contraintes[:5]
        })

    # Infos métadonnées (Challenges, Repeatable, Expires)
    text_page = soup.get_text()
    nb_challenges = 0
    m = re.search(r'Challenges\s*(\d+)', text_page)
    if m:
        nb_challenges = int(m.group(1))

    repeatable = "Repeatable" in text_page and "Repeatable-" not in text_page
    refreshes = ""
    m = re.search(r'Refreshes Every\s*([^\n]+)', text_page)
    if m:
        refreshes = m.group(1).strip()

    expiry = extract_expiry(soup)

    # Image de la carte joueur
    image_carte = ""
    for img in soup.find_all("img", src=True):
        src = img.get("src", "")
        if "futgg-player-item-card" in src or "player-item" in src:
            image_carte = src
            break

    slug = url.rstrip("/").split("/")[-1]

    recompenses_clean = deduplicar_recompenses(recompenses)
    return {
        "id": f"sbc_{slug}",
        "slug": slug,
        "titre": titre,
        "description_courte": desc[:200] if desc else titre,
        "url_futgg": url,
        "image_carte": image_carte,
        "recompense_principale": recompenses_clean[0] if recompenses_clean else "",
        "recompenses": recompenses_clean[:3],
        "nb_segments": nb_challenges or len(segments),
        "segments": segments,
        "repeatable": repeatable,
        "refreshes": refreshes,
        "expiration_texte": normaliser_expiry(expiry),
        "statut": "actif",
        "date_scrape": now_iso(),
        # Champs FC Pulse à remplir manuellement
        "priorite_fc_pulse": "",
        "verdict_fc_pulse": "",
        "resume_fc_pulse": "",
    }

def scrape_sbcs():
    """Scrape tous les SBC actifs depuis la liste FUT.GG."""
    print("\n📋 SCRAPING SBC...")
    soup = get(f"{BASE}/sbc/")
    if not soup:
        return []

    # Récupérer tous les liens SBC détaillés
    links = extract_links(soup, r'/sbc/(players|upgrades|challenges|icons|swaps)/26-')
    print(f"  {len(links)} SBC trouvés")

    sbcs = []
    for link in links[:30]:  # Limiter à 30 pour éviter le blocage
        sbc = scrape_sbc_detail(link)
        if sbc and sbc["titre"]:
            sbcs.append(sbc)

    # Aussi récupérer la catégorie "expiring soon" qui est prioritaire
    soup_exp = get(f"{BASE}/sbc/category/expiring-soon/")
    if soup_exp:
        exp_links = extract_links(soup_exp, r'/sbc/(players|upgrades|challenges)/26-')
        for link in exp_links[:10]:
            if link not in [s["url_futgg"] for s in sbcs]:
                sbc = scrape_sbc_detail(link)
                if sbc and sbc["titre"]:
                    sbc["expires_soon"] = True
                    sbcs.append(sbc)

    return sbcs

# ──────────────────────────────────────────────────────────
# SCRAPER OBJECTIFS
# ──────────────────────────────────────────────────────────

def scrape_objectif_detail(url):
    """Scrape une page de détail Objectif."""
    print(f"  → Objectif: {url.split('/')[-1][:40]}")
    soup = get(url)
    if not soup:
        return None

    title_el = soup.find("h1")
    titre = clean(title_el.get_text()) if title_el else ""
    titre = re.sub(r'\s*-\s*EA SPORTS FC 26.*', '', titre).strip()

    desc = ""
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        t = clean(p.get_text())
        if len(t) > 30 and "FUT.GG" not in t and "untradeable" in t.lower() or len(t) > 50:
            desc = t
            break

    # Récompenses
    recompenses = []
    for img in soup.find_all("img", alt=True):
        alt = img.get("alt", "")
        if any(x in alt for x in ["Pack", "SP", "Player", "Evolution", "Evo"]):
            if alt not in recompenses:
                recompenses.append(alt)

    # Tâches
    taches = []
    task_headers = soup.find_all("h4")
    for h in task_headers:
        titre_tache = clean(h.get_text())
        if not titre_tache or len(titre_tache) > 80:
            continue
        # Description de la tâche (paragraphe suivant)
        desc_tache = ""
        next_p = h.find_next("p")
        if next_p:
            desc_tache = clean(next_p.get_text())
        # Récompense de la tâche
        recomp_tache = ""
        next_img = h.find_next("img", alt=True)
        if next_img:
            recomp_tache = next_img.get("alt", "")

        if titre_tache and titre_tache not in ["Rewards", "Challenges"]:
            taches.append({
                "titre": titre_tache,
                "description": desc_tache[:200] if desc_tache else titre_tache,
                "recompense": recomp_tache,
            })

    text_page = soup.get_text()

    # XP / Season Points
    xp_total = 0
    sp_matches = re.findall(r'(\d+)\s*SP', text_page)
    if sp_matches:
        try:
            xp_total = max(int(x) for x in sp_matches)
        except:
            pass

    # Mode requis
    mode_requis = []
    modes_keywords = ["Squad Battles", "Rivals", "Champions", "Rush", "Live Events",
                      "Live Friendly", "Flash Rush", "Gauntlet"]
    for mode in modes_keywords:
        if mode.lower() in text_page.lower():
            mode_requis.append(mode)

    online = bool(mode_requis and not any(m in mode_requis for m in ["Squad Battles"]))
    solo = "Squad Battles" in mode_requis

    expiry = extract_expiry(soup)
    slug = url.rstrip("/").split("/")[-1]

    # Déterminer la catégorie depuis l'URL
    categorie = "Objectif"
    if "/campaigns/" in url: categorie = "Campagne"
    elif "/live-events/" in url: categorie = "Événement Live"
    elif "/milestones/" in url: categorie = "Jalon"
    elif "/seasonal/" in url: categorie = "Saisonnier"
    elif "/foundations/" in url: categorie = "Fondations"
    elif "/challengers/" in url: categorie = "Challengers"

    recompenses_clean = deduplicar_recompenses(recompenses)
    return {
        "id": f"obj_{slug}",
        "slug": slug,
        "titre": titre,
        "categorie": categorie,
        "description_courte": desc[:200] if desc else titre,
        "url_futgg": url,
        "mode_requis": list(set(mode_requis))[:3],
        "solo_friendly": solo,
        "online_required": online and not solo,
        "nb_taches": len(taches),
        "taches": taches[:8],
        "recompenses": recompenses_clean[:5],
        "xp_total": xp_total,
        "expiration_texte": normaliser_expiry(expiry),
        "statut": "actif",
        "date_scrape": now_iso(),
        # Champs FC Pulse
        "priorite_fc_pulse": "",
        "verdict_fc_pulse": "",
        "resume_fc_pulse": "",
    }

def scrape_objectifs():
    """Scrape tous les objectifs actifs."""
    print("\n🎯 SCRAPING OBJECTIFS...")
    soup = get(f"{BASE}/objectives/")
    if not soup:
        return []

    # Récupérer tous les liens d'objectifs
    patterns = [
        r'/objectives/campaigns/\d+',
        r'/objectives/live-events/\d+',
        r'/objectives/milestones/\d+',
        r'/objectives/seasonal/\d+',
        r'/objectives/challengers/\d+',
    ]
    links = []
    for p in patterns:
        links.extend(extract_links(soup, p))
    links = list(dict.fromkeys(links))  # dédupliquer en conservant l'ordre

    # Aussi récupérer les "expiring soon"
    soup_exp = get(f"{BASE}/objectives/expiring-soon/")
    if soup_exp:
        for p in patterns:
            for link in extract_links(soup_exp, p):
                if link not in links:
                    links.insert(0, link)  # priorité aux urgents

    print(f"  {len(links)} objectifs trouvés")

    objectifs = []
    for link in links[:25]:
        obj = scrape_objectif_detail(link)
        if obj and obj["titre"]:
            objectifs.append(obj)

    return objectifs

# ──────────────────────────────────────────────────────────
# SCRAPER ÉVOLUTIONS
# ──────────────────────────────────────────────────────────

def scrape_evo_detail(url):
    """Scrape une page de détail Évolution."""
    print(f"  → Évo: {url.split('/')[-1][:40]}")
    soup = get(url)
    if not soup:
        return None

    title_el = soup.find("h1")
    titre = clean(title_el.get_text()) if title_el else ""
    titre = re.sub(r'\s*-\s*EA SPORTS FC 26.*', '', titre).strip()

    # Description
    desc = ""
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        t = clean(p.get_text())
        if len(t) > 30 and "FUT.GG" not in t:
            desc = t
            break

    text_page = soup.get_text()

    # Coût
    cout_credits = 0
    cout_points = 0
    gratuit = "Free" in text_page

    m = re.search(r'([\d,]+)\s*(?:Coins?|FC Coin)', text_page)
    if m:
        try:
            cout_credits = int(m.group(1).replace(",", ""))
        except:
            pass

    m = re.search(r'(\d+)\s*(?:FC )?Points?', text_page)
    if m:
        try:
            cout_points = int(m.group(1))
        except:
            pass

    # Boosts / Upgrades
    boosts = []
    boost_section = soup.find(string=re.compile("Evolution Upgrades|Upgrades", re.IGNORECASE))
    if boost_section:
        parent = boost_section.parent if boost_section else None
        # Chercher les éléments boosts (+X stat)
        all_text = soup.get_text()
        boost_patterns = re.findall(r'\+(\d+)\s+([A-Za-z\s]+?)(?=\+|\d{2,3}|$)', all_text[:3000])
        seen = set()
        for val, stat in boost_patterns[:10]:
            stat_clean = stat.strip()
            if stat_clean and len(stat_clean) > 2 and stat_clean not in seen:
                seen.add(stat_clean)
                boosts.append({"stat": stat_clean, "valeur": f"+{val}"})

    # Conditions d'éligibilité
    conditions = []
    req_keywords = {
        "Max. OVR": r'Overall[^\n]*Max\.\s*(\d+)',
        "Max OVR": r'Max\.\s*(\d+)',
        "Max PS": r'Max PS\s*(\d+)',
        "Max PS+": r'Max PS\+\s*(\d+)',
        "Excluded": r'Excluded[^\n]+?([A-Z][a-zA-Z\s]+)',
        "Position exclus": r'Excluded Position\s*([A-Z]{2,})',
    }
    for label, pattern in req_keywords.items():
        m = re.search(pattern, text_page)
        if m:
            conditions.append(f"{label}: {m.group(1).strip()}")

    # Tâches (Levels)
    taches = []
    levels = soup.find_all(string=re.compile(r"Level \d+", re.IGNORECASE))
    for lvl in levels[:5]:
        parent = lvl.parent
        if parent:
            desc_tache = ""
            next_p = parent.find_next("p")
            if next_p:
                desc_tache = clean(next_p.get_text())
            challenge_txt = ""
            # Chercher "Play X matches" dans les éléments suivants
            all_txt = parent.get_text()
            m_play = re.search(r'(Play \d+[^.]+\.)', all_txt)
            if m_play:
                challenge_txt = m_play.group(1)
            niveau = re.search(r'Level (\d+)', str(lvl))
            taches.append({
                "niveau": int(niveau.group(1)) if niveau else len(taches)+1,
                "description": challenge_txt or desc_tache[:150],
            })

    # Difficulté communautaire
    difficulte = ""
    m = re.search(r'Completion Difficulty\s*\n?\s*([A-Za-z]+)', text_page)
    if m:
        difficulte = m.group(1)

    # Expiration
    expiry_submit = ""
    m = re.search(r'Submit by[^\n]*in\s+(\d+)\s+days?', text_page, re.IGNORECASE)
    if m:
        expiry_submit = f"Submit dans {m.group(1)} jours"

    expiry_expiry = ""
    m = re.search(r'Expiry[^\n]*in\s+(\d+)\s+days?', text_page, re.IGNORECASE)
    if m:
        expiry_expiry = f"Expire dans {m.group(1)} jours"

    slug = url.rstrip("/").split("/")[-1]

    # Extraire l'ID numérique pour identifier l'évolution
    m_id = re.search(r'/evolutions/(\d+)', url)
    evo_id = m_id.group(1) if m_id else slug

    return {
        "id": f"evo_{evo_id}",
        "slug": slug,
        "titre": titre,
        "description_courte": desc[:200] if desc else titre,
        "url_futgg": url,
        "cout_credits": cout_credits,
        "cout_points": cout_points,
        "gratuit": gratuit and cout_credits == 0 and cout_points == 0,
        "difficulte_communaute": normaliser_difficulte(difficulte),
        "conditions_eligibilite": normaliser_conditions(conditions),
        "boosts": boosts[:8],
        "taches": taches,
        "date_soumission": normaliser_expiry(expiry_submit) or expiry_submit,
        "date_expiration": normaliser_expiry(expiry_expiry) or expiry_expiry,
        "statut": "actif",
        "date_scrape": now_iso(),
        # Champs FC Pulse
        "priorite_fc_pulse": "",
        "verdict_fc_pulse": "",
        "resume_fc_pulse": "",
    }

def scrape_evolutions():
    """Scrape toutes les évolutions actives."""
    print("\n⚡ SCRAPING ÉVOLUTIONS...")
    soup = get(f"{BASE}/evolutions/")
    if not soup:
        return []

    links = extract_links(soup, r'/evolutions/\d+-')
    # Exclure les liens de sous-pages (eligible-players, etc.)
    links = [l for l in links if not any(
        x in l for x in ["eligible-players", "evolved-players", "trending"]
    )]
    print(f"  {len(links)} évolutions trouvées")

    evolutions = []
    for link in links[:20]:
        evo = scrape_evo_detail(link)
        if evo and evo["titre"]:
            evolutions.append(evo)

    return evolutions

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────

def sauvegarder(data, filename):
    """Sauvegarde les données en JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {filename} — {len(data)} entrées")

def main():
    print("=" * 60)
    print("  FC Pulse — Scraper FUT.GG")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 60)

    # ── SBC ──────────────────────────────────────────────
    sbcs = scrape_sbcs()
    sauvegarder(sbcs, "sbcs.json")

    # ── Objectifs ────────────────────────────────────────
    objectifs = scrape_objectifs()
    sauvegarder(objectifs, "objectifs.json")

    # ── Évolutions ───────────────────────────────────────
    evolutions = scrape_evolutions()
    sauvegarder(evolutions, "evolutions.json")

    # ── Résumé ───────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"✅ Terminé — {datetime.now().strftime('%H:%M:%S')}")
    print(f"   SBC        : {len(sbcs)}")
    print(f"   Objectifs  : {len(objectifs)}")
    print(f"   Évolutions : {len(evolutions)}")
    print()
    print("📝 Ajoute tes verdicts FC Pulse dans les JSON :")
    print('   "priorite_fc_pulse": "haute" | "moyenne" | "basse"')
    print('   "verdict_fc_pulse":  "rentable" | "interessant" | "situationnel" | "dispensable"')
    print('   "resume_fc_pulse":   "ton analyse ici..."')
    print("=" * 60)

if __name__ == "__main__":
    main()


# ──────────────────────────────────────────────────────────
# TÉLÉCHARGEMENT D'IMAGES LOCAL
# ──────────────────────────────────────────────────────────

import os
import urllib.request
import hashlib

IMG_DIR = "images_live"

def download_image(url, item_id, retries=2):
    """Télécharge une image et la sauvegarde localement."""
    if not url or url.startswith('data:'):
        return None
    os.makedirs(IMG_DIR, exist_ok=True)
    ext = url.split('?')[0].split('.')[-1].lower()
    if ext not in ['png','jpg','jpeg','webp','gif']:
        ext = 'webp'
    filename = f"{IMG_DIR}/{item_id}.{ext}"
    if os.path.exists(filename):
        return filename
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://www.fut.gg/',
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                with open(filename, 'wb') as f:
                    f.write(resp.read())
            return filename
        except Exception as e:
            print(f"    ⚠ Image fail ({attempt+1}): {e}")
            time.sleep(0.5)
    return None

def download_all_images(data, prefix):
    """Télécharge les images d'une liste d'items."""
    print(f"  📥 Téléchargement images {prefix}...")
    count = 0
    for item in data:
        if item.get('image_carte'):
            local = download_image(item['image_carte'], f"{prefix}_{item.get('id','x')}")
            if local:
                item['image_locale'] = local
                count += 1
    print(f"  ✅ {count}/{len(data)} images téléchargées")

