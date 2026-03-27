    // ════════════════════════════════════════════════════════
    // ÉTAT GLOBAL
    // ════════════════════════════════════════════════════════
    let allPlayers = [];
    let filteredPlayers = [];
    let currentSort = 'note';
    let currentPage = 'players';
    let prevPage = 'players';
    let renderOffset = 0;
    const PAGE_SIZE = 40;
    let isLoadingMore = false;
    let currentDetailId = null;
    let compareSlots = [null, null];
    let currentPickerSlot = 0;
    let favorites = JSON.parse(localStorage.getItem('fcpulse_favs') || '[]');

    // ════════════════════════════════════════════════════════
    // CHARGEMENT DONNÉES
    // ════════════════════════════════════════════════════════
    async function loadData() {
      try {
        const res = await fetch('players_clean.json');
        if (!res.ok) throw new Error('Fichier non trouvé');
        allPlayers = await res.json();
        filteredPlayers = [...allPlayers];
        populateFilters();
        applyFilters();
        setupIntersectionObserver();
      } catch (e) {
        // Mode démo avec 10 joueurs hardcodés
        allPlayers = getDemoPlayers();
        filteredPlayers = [...allPlayers];
        populateFilters();
        applyFilters();
        setupIntersectionObserver();
        console.log('Mode démo activé — placer players_clean.json dans le même dossier');
      }
    }

    function getDemoPlayers() {
      return [
        { id: 209331, slug: 'mohamed-salah', nom: 'Mohamed Salah', genre: 'Masculin', note: 91, tier: 'Élite', poste: 'MD', poste_fr: 'Milieu Droit', postes_alt: ['AD'], club: 'Liverpool', ligue: 'Premier League', nationalite: 'Égypte', rarete: 'Or Rare', rarete_couleur: { bg: '#c8a84b', text: '#1a1000' }, image_carte: 'https://ratings-images-prod.pulse.ea.com/FC26/components/items/209331_en.webp', image_visage: '', stats: { vitesse: 89, tir: 88, passes: 86, dribble: 90, defense: 45, physique: 76 }, stats_detail: { acceleration: 88, vitesse_pointe: 89, finition: 94, puissance_tir: 83, tirs_loin: 78, vista: 86, passes_courtes: 88, passes_longues: 81, dribbles: 90, agilite: 86, equilibre: 91, reactivite: 94, controle_ballon: 90, interceptions: 55, conscience_def: 38, tacle_debout: 43, detente: 79, endurance: 88, force: 75, gk_plongeon: null, gk_prise_balle: null, gk_degagement: null, gk_placement: null, gk_reflexes: null }, meta: { age: 33, taille_cm: 175, poids_kg: 72, pied_fort: 'Gauche', mauvais_pied: 3, gestes_techniques: 4 }, playstyles: ['Tir Enroulé+', 'Premier Contact', 'Décisif', 'Inventif', 'Tir Rasant', 'Technique', 'Passe Fouettée'], profil: 'Ailier explosif', points_forts: ['Vitesse', 'Dribble', 'Tir'], points_faibles: [], lien_ea: 'https://www.ea.com/games/ea-sports-fc/ratings/player-ratings/mohamed-salah/209331', search_index: 'mohamed salah liverpool premier league milieu droit égypte' },
        { id: 231747, slug: 'kylian-mbappe', nom: 'Kylian Mbappé', genre: 'Masculin', note: 91, tier: 'Élite', poste: 'ATT', poste_fr: 'Attaquant', postes_alt: ['AG', 'MG'], club: 'Real Madrid', ligue: 'La Liga', nationalite: 'France', rarete: 'Or Rare', rarete_couleur: { bg: '#c8a84b', text: '#1a1000' }, image_carte: 'https://ratings-images-prod.pulse.ea.com/FC26/components/items/231747_en.webp', image_visage: '', stats: { vitesse: 97, tir: 90, passes: 81, dribble: 92, defense: 37, physique: 76 }, stats_detail: { acceleration: 97, vitesse_pointe: 97, finition: 92, puissance_tir: 91, tirs_loin: 86, vista: 78, passes_courtes: 87, passes_longues: 74, dribbles: 92, agilite: 93, equilibre: 82, reactivite: 91, controle_ballon: 93, interceptions: 38, conscience_def: 26, tacle_debout: 34, detente: 90, endurance: 83, force: 77, gk_plongeon: null, gk_prise_balle: null, gk_degagement: null, gk_placement: null, gk_reflexes: null }, meta: { age: 26, taille_cm: 182, poids_kg: 75, pied_fort: 'Droit', mauvais_pied: 4, gestes_techniques: 5 }, playstyles: ['Pas Rapide+', 'Acrobatique', 'Tir Enroulé', 'Premier Contact', 'Décisif', 'Tir Rasant', 'Rapide'], profil: 'Attaquant de pointe', points_forts: ['Finition', 'Vitesse', 'Jeu en équipe'], points_faibles: ['Défense'], lien_ea: 'https://www.ea.com/games/ea-sports-fc/ratings/player-ratings/kylian-mbappe/231747', search_index: 'kylian mbappé real madrid la liga attaquant france' },
        { id: 239085, slug: 'erling-haaland', nom: 'Erling Haaland', genre: 'Masculin', note: 90, tier: 'Élite', poste: 'ATT', poste_fr: 'Attaquant', postes_alt: [], club: 'Manchester City', ligue: 'Premier League', nationalite: 'Norvège', rarete: 'Or Rare', rarete_couleur: { bg: '#c8a84b', text: '#1a1000' }, image_carte: 'https://ratings-images-prod.pulse.ea.com/FC26/components/items/239085_en.webp', image_visage: '', stats: { vitesse: 86, tir: 91, passes: 70, dribble: 80, defense: 45, physique: 88 }, stats_detail: { acceleration: 85, vitesse_pointe: 86, finition: 94, puissance_tir: 94, tirs_loin: 72, vista: 62, passes_courtes: 63, passes_longues: 55, dribbles: 80, agilite: 75, equilibre: 70, reactivite: 91, controle_ballon: 79, interceptions: 39, conscience_def: 28, tacle_debout: 36, detente: 93, endurance: 80, force: 90, gk_plongeon: null, gk_prise_balle: null, gk_degagement: null, gk_placement: null, gk_reflexes: null }, meta: { age: 24, taille_cm: 194, poids_kg: 88, pied_fort: 'Gauche', mauvais_pied: 3, gestes_techniques: 3 }, playstyles: ['Forteresse Aérienne', 'Premier Contact', 'Décisif', 'Tir Enroulé', 'Tir Puissant'], profil: 'Attaquant de pointe', points_forts: ['Finition', 'Physique', 'Vitesse'], points_faibles: ['Passes'], lien_ea: 'https://www.ea.com/games/ea-sports-fc/ratings/player-ratings/erling-haaland/239085', search_index: 'erling haaland manchester city premier league attaquant norvège' },
        { id: 203376, slug: 'virgil-van-dijk', nom: 'Virgil van Dijk', genre: 'Masculin', note: 90, tier: 'Élite', poste: 'DC', poste_fr: 'Défenseur Central', postes_alt: [], club: 'Liverpool', ligue: 'Premier League', nationalite: 'Pays-Bas', rarete: 'Or Rare', rarete_couleur: { bg: '#c8a84b', text: '#1a1000' }, image_carte: 'https://ratings-images-prod.pulse.ea.com/FC26/components/items/203376_en.webp', image_visage: '', stats: { vitesse: 73, tir: 60, passes: 72, dribble: 72, defense: 90, physique: 87 }, stats_detail: { acceleration: 70, vitesse_pointe: 76, finition: 55, puissance_tir: 63, tirs_loin: 49, vista: 62, passes_courtes: 74, passes_longues: 70, dribbles: 72, agilite: 61, equilibre: 70, reactivite: 84, controle_ballon: 71, interceptions: 87, conscience_def: 89, tacle_debout: 86, detente: 90, endurance: 85, force: 91, gk_plongeon: null, gk_prise_balle: null, gk_degagement: null, gk_placement: null, gk_reflexes: null }, meta: { age: 33, taille_cm: 193, poids_kg: 92, pied_fort: 'Droit', mauvais_pied: 3, gestes_techniques: 2 }, playstyles: ['Forteresse Aérienne', 'Blocage', 'Anticipation', 'Imposant'], profil: 'Défenseur physique', points_forts: ['Défense', 'Physique'], points_faibles: ['Technique balle au pied'], lien_ea: 'https://www.ea.com/games/ea-sports-fc/ratings/player-ratings/virgil-van-dijk/203376', search_index: 'virgil van dijk liverpool premier league défenseur central pays-bas' },
        { id: 231866, slug: 'rodri', nom: 'Rodri', genre: 'Masculin', note: 90, tier: 'Élite', poste: 'MDC', poste_fr: 'Milieu Défensif Central', postes_alt: ['MC'], club: 'Manchester City', ligue: 'Premier League', nationalite: 'Espagne', rarete: 'Or Rare', rarete_couleur: { bg: '#c8a84b', text: '#1a1000' }, image_carte: 'https://ratings-images-prod.pulse.ea.com/FC26/components/items/231866_en.webp', image_visage: '', stats: { vitesse: 65, tir: 80, passes: 86, dribble: 84, defense: 86, physique: 85 }, stats_detail: { acceleration: 63, vitesse_pointe: 67, finition: 68, puissance_tir: 80, tirs_loin: 72, vista: 80, passes_courtes: 87, passes_longues: 85, dribbles: 80, agilite: 72, equilibre: 78, reactivite: 87, controle_ballon: 86, interceptions: 90, conscience_def: 88, tacle_debout: 88, detente: 80, endurance: 89, force: 85, gk_plongeon: null, gk_prise_balle: null, gk_degagement: null, gk_placement: null, gk_reflexes: null }, meta: { age: 28, taille_cm: 191, poids_kg: 82, pied_fort: 'Droit', mauvais_pied: 3, gestes_techniques: 3 }, playstyles: ['Pressing Éprouvé+', 'Interception', 'Anticipation', 'Blocage', 'Distribution'], profil: 'Sentinelle', points_forts: ['Interceptions', 'Défense', 'Distribution'], points_faibles: [], lien_ea: 'https://www.ea.com/games/ea-sports-fc/ratings/player-ratings/rodri/231866', search_index: 'rodri manchester city premier league milieu défensif espagne' },
      ];
    }

    // ════════════════════════════════════════════════════════
    // NAVIGATION
    // ════════════════════════════════════════════════════════
    // ════════════════════════════════════════════════════════
    // PROMPT 4 — LECTURE FOOTBALL + USAGE
    // ════════════════════════════════════════════════════════
    function statBarColor(val) {
      if (val >= 85) return '#22c55e';
      if (val >= 75) return '#86efac';
      if (val >= 65) return '#f0cc70';
      if (val >= 55) return '#f97316';
      return '#ef4444';
    }

    function buildStatsBarHTML(label, val) {
      if (!val || val === '—') return '';
      const pct = Math.min(100, Math.round((val / 99) * 100));
      const color = statBarColor(val);
      return `<div class="stat-bar-wrap">
    <span class="stat-bar-label">${label}</span>
    <div class="stat-bar-track"><div class="stat-bar-fill" style="width:${pct}%;background:${color}"></div></div>
    <span class="stat-bar-val" style="color:${color}">${val}</span>
  </div>`;
    }

    function buildProfilBlock(p) {
      const s = p.stats || {};
      const sd = p.stats_detail || {};
      const m = p.meta || {};
      const ps = (p.playstyles || []).join(' ').toLowerCase();
      const poste = p.poste;

      // ── PROFIL EMOJI
      const emojiMap = {
        GB: '🧤', DC: '🛡️', DG: '🛡️', DD: '🛡️', PDG: '🛡️', PDD: '🛡️',
        MDC: '⚙️', MC: '⚙️', MG: '🎯', MD: '🎯', MOC: '✨',
        AG: '⚡', AD: '⚡', SA: '🔥', ATT: '🔥'
      };
      const emoji = emojiMap[poste] || '⚽';

      // ── ROLES RECOMMANDÉS selon stats et poste
      const roles = [];
      if (s.vitesse >= 85 && ['AG', 'AD', 'ATT', 'SA'].includes(poste)) roles.push('Attaque rapide');
      if (s.dribble >= 85 && s.vitesse >= 80) roles.push('Dribbleur');
      if (sd.finition >= 85 || s.tir >= 85) roles.push('Finisseur');
      if (s.passes >= 85 || sd.vista >= 80) roles.push('Distributeur');
      if (s.defense >= 80 && ['DC', 'MDC', 'DG', 'DD'].includes(poste)) roles.push('Défenseur solide');
      if (sd.interceptions >= 80 || ps.includes('interception')) roles.push('Récupérateur');
      if (s.physique >= 85) roles.push('Physique dominant');
      if (sd.detente >= 82 || ps.includes('forteresse')) roles.push('Jeu aérien');
      if (ps.includes('tir en finesse') || ps.includes('finesse')) roles.push('Tir en finesse');
      if (ps.includes('passe incisive') || ps.includes('tiki taka')) roles.push('Jeu combiné');
      if (ps.includes('rapide') || ps.includes('pas rapide')) roles.push('Pressing intensif');
      if (m.gestes_techniques >= 4 && s.dribble >= 80) roles.push('Dribbleur technique');

      // ── DESCRIPTION AUTOMATIQUE selon profil
      let desc = p.profil ? `<em>${p.profil}</em>. ` : '';
      if (['ATT', 'SA'].includes(poste)) {
        if (s.vitesse >= 90) desc += 'Attaquant ultra-rapide capable de déborder les défenses en profondeur. ';
        else if (sd.finition >= 90) desc += 'Attaquant de surface redoutable, efficace dans les petits espaces. ';
        else if (s.tir >= 88 && s.physique >= 82) desc += 'Avant-centre puissant et difficile à bousculer. ';
        else desc += 'Attaquant polyvalent qui combine finition et jeu de remise. ';
      } else if (['AG', 'AD'].includes(poste)) {
        if (s.vitesse >= 90 && s.dribble >= 85) desc += 'Ailier explosif en un-contre-un, efficace en transition rapide. ';
        else if (s.passes >= 83 && sd.vista >= 78) desc += 'Ailier créatif qui joue beaucoup en combinaison. ';
        else desc += 'Ailier polyvalent capable de centrer comme de tirer. ';
      } else if (['MC', 'MOC'].includes(poste)) {
        if (s.passes >= 87 && sd.vista >= 82) desc += 'Milieu créatif, véritable cerveau du jeu offensif. ';
        else if (s.defense >= 78 && s.passes >= 82) desc += "Milieu box-to-box capable d'abattre un énorme volume de travail. ";
        else desc += 'Milieu équilibré entre construction et participation offensive. ';
      } else if (poste === 'MDC') {
        desc += 'Sentinelle devant la défense, priorité à la récupération et à la distribution courte. ';
      } else if (['DC', 'DG', 'DD'].includes(poste)) {
        if (s.vitesse >= 80 && s.defense >= 82) desc += "Défenseur mobile, à l'aise dans les duels et en phase de transition. ";
        else if (s.physique >= 88 && s.defense >= 85) desc += 'Défenseur physique dominant dans les duels aériens et au sol. ';
        else desc += 'Défenseur solide, fiable en couverture et en marquage. ';
      } else if (poste === 'GB') {
        desc += 'Gardien à analyser principalement sur les stats GK (réflexes, plongeon, placement). ';
      }

      // Infos complémentaires
      if (m.pied_fort === 'Gauche' && ['AD', 'MD'].includes(poste)) desc += '⚠️ Pied gauche pour un côté droit — profil inverti polyvalent. ';
      if (m.gestes_techniques >= 4) desc += `Gestes techniques ${m.gestes_techniques}★ — grande liberté balle au pied. `;
      if (m.mauvais_pied >= 4) desc += `Mauvais pied ${m.mauvais_pied}★ — peut jouer des deux pieds efficacement. `;

      // ── STATS VISUELLES CLÉS
      const statKeys = poste === 'GB'
        ? [['Réflexes', sd.gk_reflexes], ['Plongeon', sd.gk_plongeon], ['Placement', sd.gk_placement]]
        : [
          ['VIT', s.vitesse], ['TIR', s.tir], ['PAS', s.passes],
          ['DRI', s.dribble], ['DEF', s.defense], ['PHY', s.physique]
        ];
      const barsHTML = statKeys.map(([lbl, val]) => buildStatsBarHTML(lbl, val)).join('');

      const fortsHTML = (p.points_forts || []).map(f => `<span class="profil-fort">✓ ${f}</span>`).join('');
      const faiblesHTML = (p.points_faibles || []).map(f => `<span class="profil-faible">↓ ${f}</span>`).join('');
      const rolesHTML = roles.slice(0, 4).map(r => `<span class="profil-role-tag">${r}</span>`).join('');

      return `
    <div class="profil-block">
      <div class="profil-block-header">
        <span class="profil-block-emoji">${emoji}</span>
        <span class="profil-block-name">${p.profil || p.poste_fr || poste}</span>
        <span class="profil-block-role">${p.tier || ''}</span>
      </div>
      <div class="profil-block-desc">${desc}</div>
      ${barsHTML}
      <div class="profil-tags" style="margin-top:8px">
        ${fortsHTML}${faiblesHTML}${rolesHTML}
      </div>
    </div>`;
    }

    function showPage(name) {
      document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('page-' + name).classList.add('active');
      document.getElementById('nav-' + name)?.classList.add('active');
      if (name !== 'detail') currentPage = name;
      if (name === 'favorites') renderFavorites();
      if (name === 'compare') renderCompareTable();
    }

    function showDetail(id) {
      prevPage = currentPage;
      currentDetailId = id;
      const p = allPlayers.find(x => x.id === id);
      if (!p) return;
      document.getElementById('detail-header-nom').textContent = p.nom;
      document.getElementById('detail-content').innerHTML = buildDetailHTML(p);
      updateFavBtn(p.id);
      document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
      document.getElementById('page-detail').classList.add('active');
      window.scrollTo(0, 0);
    }

    function goBack() {
      showPage(prevPage);
    }

    // ════════════════════════════════════════════════════════
    // FILTRES & RECHERCHE
    // ════════════════════════════════════════════════════════
    function populateFilters() {
      const ligues = [...new Set(allPlayers.map(p => p.ligue).filter(Boolean))].sort();
      const nations = [...new Set(allPlayers.map(p => p.nationalite).filter(Boolean))].sort();
      const sel1 = document.getElementById('f-ligue');
      const sel2 = document.getElementById('f-nation');
      ligues.forEach(l => { const o = document.createElement('option'); o.value = l; o.textContent = l; sel1.appendChild(o); });
      nations.forEach(n => { const o = document.createElement('option'); o.value = n; o.textContent = n; sel2.appendChild(o); });
    }

    function toggleFilters() {
      const panel = document.getElementById('filters-panel');
      const btn = document.getElementById('filter-toggle-btn');
      panel.classList.toggle('open');
      btn.classList.toggle('active');
    }

    let searchTimer;
    function onSearch() {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(applyFilters, 150);
    }

    function applyFilters() {
      const q = document.getElementById('search-input').value.toLowerCase().trim();
      const poste = document.getElementById('f-poste').value;
      const rarete = document.getElementById('f-rarete').value;
      const ligue = document.getElementById('f-ligue').value;
      const nation = document.getElementById('f-nation').value;
      const pied = document.getElementById('f-pied').value;
      const noteMin = parseInt(document.getElementById('f-note-min').value);

      filteredPlayers = allPlayers.filter(p => {
        if (q && !p.search_index?.includes(q) && !p.nom?.toLowerCase().includes(q)) return false;
        if (poste && p.poste !== poste) return false;
        if (rarete && p.rarete !== rarete) return false;
        if (ligue && p.ligue !== ligue) return false;
        if (nation && p.nationalite !== nation) return false;
        if (pied && p.meta?.pied_fort !== pied) return false;
        if (p.note < noteMin) return false;
        // Quick filters
        if (quickPostFilter && quickPostFilter !== 'all') {
          if (p.poste !== quickPostFilter && !(p.postes_alt || []).includes(quickPostFilter)) return false;
        }
        if (quickRareteFilter && p.rarete !== quickRareteFilter) return false;
        if (quickLigueFilter && p.ligue !== quickLigueFilter) return false;
        return true;
      });

      sortPlayers();
      renderOffset = 0;
      document.getElementById('players-list').innerHTML = '';
      document.getElementById('result-count').textContent = filteredPlayers.length.toLocaleString('fr-FR') + ' joueurs';
      renderNextBatch();
    }

    let sortDir = 'desc';
    let quickPostFilter = 'all';
    let quickRareteFilter = '';
    let quickLigueFilter = '';

    const SORT_LABELS = { note: 'Note', vitesse: 'Vitesse', tir: 'Tir', passes: 'Passes', dribble: 'Dribble', defense: 'Défense', physique: 'Physique', age: 'Âge' };
    // Direction par défaut : 'asc' pour l'âge, 'desc' pour tout le reste
    const SORT_DEFAULT_DIR = { age: 'asc' };

    function setSort(key, el) {
      if (currentSort === key) {
        // Même colonne → toggle direction
        sortDir = sortDir === 'desc' ? 'asc' : 'desc';
      } else {
        // Nouvelle colonne → direction par défaut
        currentSort = key;
        sortDir = SORT_DEFAULT_DIR[key] || 'desc';
      }
      // Réinitialiser tous les chips
      document.querySelectorAll('.sort-chip').forEach(c => {
        c.classList.remove('active');
        const k = c.dataset.key;
        const defaultDir = SORT_DEFAULT_DIR[k] || 'desc';
        c.textContent = SORT_LABELS[k] + (defaultDir === 'asc' ? ' ↑' : '');
      });
      // Activer le chip courant avec flèche
      const arrow = sortDir === 'asc' ? ' ↑' : ' ↓';
      el.classList.add('active');
      el.dataset.dir = sortDir;
      el.textContent = (SORT_LABELS[key] || key) + arrow;
      applyFilters();
    }

    function setQuickFilter(val, el) {
      quickPostFilter = val;
      quickRareteFilter = '';
      quickLigueFilter = '';
      document.querySelectorAll('.qf-pill').forEach(p => p.classList.remove('on'));
      el.classList.add('on');
      applyFilters();
    }

    function setRarete(val, el) {
      quickRareteFilter = quickRareteFilter === val ? '' : val;
      quickPostFilter = 'all';
      quickLigueFilter = '';
      document.querySelectorAll('.qf-pill').forEach(p => p.classList.remove('on'));
      if (quickRareteFilter) el.classList.add('on');
      else document.querySelector('#quick-filters .qf-pill').classList.add('on');
      applyFilters();
    }

    function setTopLigue(val, el) {
      quickLigueFilter = quickLigueFilter === val ? '' : val;
      quickPostFilter = 'all';
      quickRareteFilter = '';
      // Désactiver postes/raretés
      document.querySelectorAll('#quick-filters .qf-pill').forEach(p => p.classList.remove('on'));
      document.querySelector('#quick-filters .qf-pill').classList.add('on');
      // Activer/désactiver le chip ligue
      document.querySelectorAll('#quick-filters-leagues .qf-pill').forEach(p => p.classList.remove('on'));
      if (quickLigueFilter) el.classList.add('on');
      applyFilters();
    }

    function sortPlayers() {
      filteredPlayers.sort((a, b) => {
        let va, vb;
        if (currentSort === 'age') { va = a.meta?.age || 99; vb = b.meta?.age || 99; }
        else if (currentSort === 'note') { va = a.note; vb = b.note; }
        else { va = a.stats?.[currentSort] || 0; vb = b.stats?.[currentSort] || 0; }
        return sortDir === 'asc' ? va - vb : vb - va;
      });
    }

    // ════════════════════════════════════════════════════════
    // RENDU LISTE (virtuel, batches)
    // ════════════════════════════════════════════════════════
    function renderNextBatch() {
      if (isLoadingMore) return;
      isLoadingMore = true;
      const list = document.getElementById('players-list');
      const batch = filteredPlayers.slice(renderOffset, renderOffset + PAGE_SIZE);
      const frag = document.createDocumentFragment();
      batch.forEach(p => {
        const el = document.createElement('div');
        el.className = 'player-row';
        el.onclick = () => showDetail(p.id);
        el.innerHTML = buildPlayerRowHTML(p);
        frag.appendChild(el);
      });
      list.appendChild(frag);
      renderOffset += batch.length;
      document.getElementById('load-more-spinner').classList.toggle('visible', renderOffset < filteredPlayers.length);
      isLoadingMore = false;
    }

    function buildPlayerRowHTML(p) {
      const rareteBg = p.rarete_couleur?.bg || '#666';
      const statsKeys = ['vitesse', 'tir', 'passes', 'dribble', 'defense', 'physique'];
      const statsLabels = ['VIT', 'TIR', 'PAS', 'DRI', 'DEF', 'PHY'];
      const statsHtml = statsKeys.map((k, i) => {
        const v = p.stats?.[k] || '—';
        const col = (typeof v === 'number')
          ? (v >= 85 ? '#22c55e' : v >= 75 ? '#86efac' : v >= 65 ? '#f0cc70' : v >= 55 ? '#f97316' : '#ef4444')
          : 'var(--text3)';
        return `<div class="stat-mini"><span class="stat-mini-val" style="color:${col}">${v}</span><span class="stat-mini-lbl">${statsLabels[i]}</span></div>`;
      }).join('');

      // Carte image ou fallback avec couleur rareté
      const cardBg = p.rarete === 'Or Rare' ? 'linear-gradient(160deg,#3d2e0a,#c8a84b,#3d2e0a)' :
        p.rarete === 'Argent Rare' ? 'linear-gradient(160deg,#1a1a22,#8a8aa0,#1a1a22)' :
          'linear-gradient(160deg,#2a1a0a,#a06030,#2a1a0a)';

      const noteColor = p.rarete === 'Or Rare' ? 'var(--gold2)' : p.rarete === 'Argent Rare' ? '#b8b8c8' : '#c87840';

      return `
    <div class="player-card-mini" style="background:${cardBg}">
      <img src="${p.image_carte}" alt="${p.nom}" onerror="this.onerror=null;this.style.display='none';this.nextElementSibling.style.display='flex'"
           style="width:100%;height:100%;object-fit:cover;object-position:top center;">
      <div class="card-mini-fallback" style="display:none;background:${cardBg};position:absolute;inset:0;flex-direction:column;align-items:center;justify-content:center;">
        <span style="font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:20px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,0.7)">${p.note}</span>
        <span style="font-size:10px;color:rgba(255,255,255,0.7);font-weight:700">${p.poste}</span>
      </div>
    </div>
    <div class="player-info">
      <div class="player-name">${p.nom}</div>
      <div class="player-meta">
        <span class="player-poste">${p.poste}</span>
        <span class="player-club">${p.club || '—'}</span>
        <span class="player-nat">${p.nationalite || ''}</span>
      </div>
      <div class="player-stats-mini">${statsHtml}</div>
    </div>
    <div class="player-right-col">
      <span class="player-ovr" style="color:${noteColor}">${p.note}</span>
      <div class="player-rarete-dot" style="background:${rareteBg};box-shadow:0 0 6px ${rareteBg}" title="${p.rarete}"></div>
    </div>`;
    }

    function setupIntersectionObserver() {
      const sentinel = document.getElementById('scroll-sentinel');
      const obs = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && renderOffset < filteredPlayers.length) {
          renderNextBatch();
        }
      }, { rootMargin: '200px' });
      obs.observe(sentinel);
    }

    // ════════════════════════════════════════════════════════
    // PAGE DETAIL
    // ════════════════════════════════════════════════════════
    function buildDetailHTML(p) {
      const rareteBg = p.rarete === 'Or Rare' ? 'linear-gradient(135deg,#3d2e0a,#7c5a1a,#c8a84b,#7c5a1a,#3d2e0a)' :
        p.rarete === 'Argent Rare' ? 'linear-gradient(135deg,#1a1a22,#4a4a5a,#8a8aa0,#4a4a5a,#1a1a22)' :
          'linear-gradient(135deg,#2a1a0a,#5a3010,#a06030,#5a3010,#2a1a0a)';
      const rClass = p.rarete === 'Or Rare' ? 'rarete-badge-gold' : p.rarete === 'Argent Rare' ? 'rarete-badge-silver' : 'rarete-badge-bronze';

      // Stats principales
      // Stats principales : grille de cartes colorées
      const statColor = v => v >= 85 ? '#22c55e' : v >= 75 ? '#86efac' : v >= 65 ? '#f0cc70' : v >= 55 ? '#f97316' : '#ef4444';
      const statsMainHtml = [
        ['VIT', 'vitesse'], ['TIR', 'tir'], ['PAS', 'passes'],
        ['DRI', 'dribble'], ['DEF', 'defense'], ['PHY', 'physique']
      ].map(([lbl, k]) => {
        const v = p.stats?.[k] || 0;
        const col = statColor(v);
        return `<div class="stat-main-card" style="--stat-color:${col}">
      <div class="stat-main-val" style="color:${col}">${v}</div>
      <div class="stat-main-lbl">${lbl}</div>
    </div>`;
      }).join('');

      // Stats détaillées selon poste
      let statsDetailHtml = '';
      const isGK = p.poste === 'GB';
      const detailGroups = isGK ? [
        {
          title: 'Attributs Gardien', stats: [
            { k: 'gk_plongeon', l: 'Plongeon' }, { k: 'gk_prise_balle', l: 'Prise de balle' },
            { k: 'gk_degagement', l: 'Dégagement' }, { k: 'gk_placement', l: 'Placement' }, { k: 'gk_reflexes', l: 'Réflexes' }
          ]
        }
      ] : [
        { title: 'Vitesse', stats: [{ k: 'acceleration', l: 'Accélération' }, { k: 'vitesse_pointe', l: 'Vitesse de pointe' }] },
        { title: 'Tir', stats: [{ k: 'finition', l: 'Finition' }, { k: 'puissance_tir', l: 'Puissance de tir' }, { k: 'tirs_loin', l: 'Tirs de loin' }] },
        { title: 'Passes', stats: [{ k: 'vista', l: 'Vista' }, { k: 'passes_courtes', l: 'Passes courtes' }, { k: 'passes_longues', l: 'Passes longues' }] },
        { title: 'Dribble', stats: [{ k: 'dribbles', l: 'Dribbles' }, { k: 'agilite', l: 'Agilité' }, { k: 'equilibre', l: 'Équilibre' }, { k: 'reactivite', l: 'Réactivité' }, { k: 'controle_ballon', l: 'Contrôle du ballon' }] },
        { title: 'Défense', stats: [{ k: 'interceptions', l: 'Interceptions' }, { k: 'conscience_def', l: 'Conscience défensive' }, { k: 'tacle_debout', l: 'Tacle debout' }] },
        { title: 'Physique', stats: [{ k: 'detente', l: 'Détente' }, { k: 'endurance', l: 'Endurance' }, { k: 'force', l: 'Force' }] },
      ];

      detailGroups.forEach(g => {
        const rows = g.stats.map(s => {
          const v = p.stats_detail?.[s.k];
          if (v === null || v === undefined) return '';
          const pct = Math.round((v / 100) * 100);
          const color = v >= 85 ? '#22c55e' : v >= 75 ? '#86efac' : v >= 65 ? '#f0cc70' : v >= 55 ? '#f97316' : '#ef4444';
          return `<div class="stat-bar-row">
        <span class="stat-bar-label">${s.l}</span>
        <div class="stat-bar-track"><div class="stat-bar-fill" style="width:${pct}%;background:${color}"></div></div>
        <span class="stat-bar-val" style="color:${color}">${v}</span>
      </div>`;
        }).join('');
        if (rows) {
          statsDetailHtml += `<div class="detail-section"><div class="detail-section-title">${g.title}</div>${rows}</div><div style="height:12px"></div>`;
        }
      });

      // PlayStyles
      const psHtml = (p.playstyles || []).map(ps => {
        const isPlus = ps.endsWith('+');
        return `<span class="playstyle-chip ${isPlus ? 'plus' : ''}">${ps}</span>`;
      }).join('');

      // Postes alternatifs
      const altPosHtml = (p.postes_alt || []).map(pos => `<span class="badge badge-accent">${pos}</span>`).join('');

      return `
    <div class="detail-hero">
      <div class="detail-card-img-wrap">
        ${(() => {
          const imgSrc = p.image_carte || p.image_visage;
          if (!imgSrc) return '';
          return `<img src="${imgSrc}" alt="${p.nom}" class="detail-card-img"
            onerror="this.onerror=null;this.style.display='none';this.nextElementSibling.style.display='flex'"
            style="display:block">`;
        })()}
        <div class="detail-card-fallback" style="display:${(p.image_carte || p.image_visage) ? 'none' : 'flex'};background:${rareteBg}">
          <div class="ovr-big">${p.note}</div>
          <div class="pos-big">${p.poste}</div>
        </div>
      </div>
      <div class="detail-hero-info">
        <div class="detail-nom">${p.nom}</div>
        <div class="detail-club-line">${p.club || '—'} · ${p.ligue || '—'}</div>
        <div class="detail-badges" style="margin-top:8px">
          <span class="badge ${rClass}">${p.rarete}</span>
          <span class="badge badge-accent">${p.poste_fr || p.poste}</span>
          ${altPosHtml}
          <span class="badge badge-green">${p.tier}</span>
        </div>
        <div style="margin-top:6px;font-size:12px;color:var(--text3)">${p.nationalite || ''}</div>
      </div>
    </div>

    ${buildProfilBlock(p)}

    <div class="detail-section" style="padding-top:16px">
      <div class="detail-section-title">Stats principales</div>
      <div class="stats-main-grid">${statsMainHtml}</div>
    </div>

    ${statsDetailHtml}

    ${psHtml ? `<div class="detail-section"><div class="detail-section-title">Play Styles</div><div class="playstyles-grid">${psHtml}</div></div><div style="height:16px"></div>` : ''}

    <div class="detail-section">
      <div class="detail-section-title">Profil joueur</div>
      <div class="meta-grid">
        <div class="meta-item"><div class="meta-item-label">Âge</div><div class="meta-item-value">${p.meta?.age || '—'} ans</div></div>
        <div class="meta-item"><div class="meta-item-label">Taille</div><div class="meta-item-value">${p.meta?.taille_cm ? p.meta.taille_cm + 'cm' : '—'}</div></div>
        <div class="meta-item"><div class="meta-item-label">Pied fort</div><div class="meta-item-value">${p.meta?.pied_fort || '—'}</div></div>
        <div class="meta-item"><div class="meta-item-label">Mauvais pied</div><div class="meta-item-value">${'★'.repeat(p.meta?.mauvais_pied || 0) + '☆'.repeat(5 - (p.meta?.mauvais_pied || 0))}</div></div>
        <div class="meta-item"><div class="meta-item-label">Gestes tech.</div><div class="meta-item-value">${'★'.repeat(p.meta?.gestes_techniques || 0) + '☆'.repeat(5 - (p.meta?.gestes_techniques || 0))}</div></div>
        <div class="meta-item"><div class="meta-item-label">Poids</div><div class="meta-item-value">${p.meta?.poids_kg ? p.meta.poids_kg + 'kg' : '—'}</div></div>
      </div>
    </div>

    <div class="action-row">
      <button class="btn-primary" onclick="addToCompare(${p.id})">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M16 3h5v5M8 21H3v-5M21 3l-7 7M3 21l7-7"/></svg>
        Comparer
      </button>
      <a href="${p.lien_ea}" target="_blank" class="btn-secondary" style="text-decoration:none">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>
        EA
      </a>
    </div>
    <div style="height:8px"></div>`;
    }

    // ════════════════════════════════════════════════════════
    // FAVORIS
    // ════════════════════════════════════════════════════════
    function toggleFav(id) {
      const idx = favorites.indexOf(id);
      if (idx === -1) favorites.push(id);
      else favorites.splice(idx, 1);
      localStorage.setItem('fcpulse_favs', JSON.stringify(favorites));
    }

    function toggleFavDetail() {
      if (!currentDetailId) return;
      toggleFav(currentDetailId);
      updateFavBtn(currentDetailId);
    }

    function updateFavBtn(id) {
      const isFav = favorites.includes(id);
      const btn = document.getElementById('detail-fav-btn');
      const lbl = document.getElementById('fav-btn-label');
      if (btn) { btn.classList.toggle('fav-active', isFav); }
      if (lbl) { lbl.textContent = isFav ? 'Retiré' : 'Favoris'; }
    }

    function renderFavorites() {
      const list = document.getElementById('favorites-list');
      if (favorites.length === 0) {
        list.innerHTML = `<div class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 21l-1.45-1.32C5.4 15.36 2 12.28 2 8.5A5.5 5.5 0 017.5 3c1.74 0 3.41.81 4.5 2.09A5.99 5.99 0 0116.5 3 5.5 5.5 0 0122 8.5c0 3.78-3.4 6.86-8.55 11.18L12 21z"/></svg>
      <h3>Aucun favori</h3>
      <p>Ajoute des joueurs depuis leur fiche en appuyant sur Favoris</p>
    </div>`;
        return;
      }
      const favPlayers = favorites.map(id => allPlayers.find(p => p.id === id)).filter(Boolean);
      // Header infos
      const avgNote = Math.round(favPlayers.reduce((s, p) => s + p.note, 0) / favPlayers.length);
      list.innerHTML = `<div style="padding:10px 16px;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--border)">
    <span style="font-size:12px;color:var(--text3)">${favPlayers.length} joueur${favPlayers.length > 1 ? 's' : ''} • Note moy. <strong style="color:var(--gold2)">${avgNote}</strong></span>
    <button onclick="compareFromFavorites()" style="margin-left:auto;background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.2);color:var(--accent);border-radius:6px;padding:5px 10px;font-size:12px;font-weight:600;cursor:pointer">Comparer</button>
  </div>` + favPlayers.map(p => `
    <div class="player-row" onclick="showDetail(${p.id})">
      ${buildPlayerRowHTML(p)}
    </div>`).join('');
    }

    // ════════════════════════════════════════════════════════
    // COMPARATEUR
    // ════════════════════════════════════════════════════════
    function addToCompare(id) {
      const slot = compareSlots[0] === null ? 0 : (compareSlots[1] === null ? 1 : 0);
      compareSlots[slot] = allPlayers.find(p => p.id === id);
      showPage('compare');
      renderCompareSlots();
      renderCompareTable();
    }

    function openPlayerPicker(slot) {
      currentPickerSlot = slot;
      document.getElementById('modal-search-input').value = '';
      renderModalResults('');
      document.getElementById('player-picker-modal').classList.add('open');
    }
    function closePlayerPicker() {
      document.getElementById('player-picker-modal').classList.remove('open');
    }

    function renderModalResults(q) {
      const term = q.toLowerCase().trim();
      const results = term
        ? allPlayers.filter(p => p.nom.toLowerCase().includes(term) || p.club?.toLowerCase().includes(term)).slice(0, 30)
        : allPlayers.slice(0, 30);
      document.getElementById('modal-results').innerHTML = results.map(p => `
    <div class="modal-player-row" onclick="selectPlayerForCompare(${p.id})">
      <span class="modal-player-ovr">${p.note}</span>
      <div>
        <div class="modal-player-name">${p.nom}</div>
        <div class="modal-player-info">${p.poste} · ${p.club || ''} · ${p.nationalite || ''}</div>
      </div>
    </div>`).join('');
    }

    function selectPlayerForCompare(id) {
      compareSlots[currentPickerSlot] = allPlayers.find(p => p.id === id);
      closePlayerPicker();
      renderCompareSlots();
      renderCompareTable();
    }

    function removeFromCompare(slot) {
      compareSlots[slot] = null;
      renderCompareSlots();
      renderCompareTable();
    }

    function renderCompareSlots() {
      [0, 1].forEach(i => {
        const p = compareSlots[i];
        const el = document.getElementById(`slot-${i}`);
        if (!p) {
          el.innerHTML = `<div class="compare-slot-add"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg></div><span style="font-size:12px;color:var(--text3)">Joueur ${i + 1}</span>`;
          el.classList.remove('filled');
          el.onclick = () => openPlayerPicker(i);
        } else {
          el.innerHTML = `
        <div class="compare-slot-note">${p.note}</div>
        <div class="compare-slot-poste">${p.poste}</div>
        <div class="compare-slot-name">${p.nom}</div>
        <div style="font-size:11px;color:var(--text3)">${p.club || ''}</div>
        <button class="compare-remove" onclick="event.stopPropagation();removeFromCompare(${i})">Retirer</button>`;
          el.classList.add('filled');
          el.onclick = null;
        }
      });
    }

    function generateCompareSummary(a, b) {
      const keys = [['vitesse', 'vitesse'], ['tir', 'en tir'], ['passes', 'en passes'], ['dribble', 'au dribble'], ['defense', 'défensivement'], ['physique', 'physiquement']];
      let aWins = [], bWins = [];
      keys.forEach(([k, lbl]) => {
        const diff = (a.stats?.[k] || 0) - (b.stats?.[k] || 0);
        if (diff >= 5) aWins.push(lbl);
        else if (diff <= -5) bWins.push(lbl);
      });
      let txt = '';
      if (aWins.length) txt += `<strong>${a.nom}</strong> domine ${aWins.slice(0, 2).join(' et ')}. `;
      if (bWins.length) txt += `<strong>${b.nom}</strong> prend l'avantage ${bWins.slice(0, 2).join(' et ')}. `;
      if (!txt) txt = 'Les deux joueurs sont très proches sur l'ensemble des stats principales. ';
      if (a.profil && b.profil && a.profil !== b.profil) {
        txt += `Profils différents : ${a.nom} joue plutôt comme ${a.profil.toLowerCase()}, ${b.nom} comme ${b.profil.toLowerCase()}.`;
      }
      return txt;
    }

    function renderCompareTable() {
      const [a, b] = compareSlots;
      const table = document.getElementById('compare-table');
      if (!a && !b) { table.innerHTML = '<div class="loading-msg" style="padding:30px">Sélectionne deux joueurs à comparer</div>'; return; }
      if (!a || !b) { table.innerHTML = '<div class="loading-msg" style="padding:30px">Sélectionne un deuxième joueur</div>'; return; }

      // Synthèse
      const summaryBox = document.getElementById('compare-summary-box');
      if (summaryBox) summaryBox.innerHTML = '<div class="compare-summary"><div class="compare-summary-title">⚡ Synthèse FC Pulse</div><div class="compare-summary-txt">' + generateCompareSummary(a, b) + '</div></div>';

      const groups = [
        {
          title: 'Stats principales', rows: [
            { l: 'Note', va: a.note, vb: b.note },
            { l: 'Vitesse', va: a.stats?.vitesse, vb: b.stats?.vitesse },
            { l: 'Tir', va: a.stats?.tir, vb: b.stats?.tir },
            { l: 'Passes', va: a.stats?.passes, vb: b.stats?.passes },
            { l: 'Dribble', va: a.stats?.dribble, vb: b.stats?.dribble },
            { l: 'Défense', va: a.stats?.defense, vb: b.stats?.defense },
            { l: 'Physique', va: a.stats?.physique, vb: b.stats?.physique },
          ]
        },
        {
          title: 'Profil', rows: [
            { l: 'Âge', va: a.meta?.age, vb: b.meta?.age, lower: true },
            { l: 'Taille', va: a.meta?.taille_cm, vb: b.meta?.taille_cm },
            { l: 'Gestes', va: a.meta?.gestes_techniques, vb: b.meta?.gestes_techniques },
            { l: 'M. pied', va: a.meta?.mauvais_pied, vb: b.meta?.mauvais_pied },
          ]
        },
      ];

      let html = '';
      groups.forEach(g => {
        html += `<div class="compare-table-section"><div class="compare-table-title">${g.title}</div>`;
        g.rows.forEach(r => {
          const va = r.va || 0, vb = r.vb || 0;
          const aWin = r.lower ? va < vb : va > vb;
          const bWin = r.lower ? vb < va : vb > va;
          const diffVal = Math.abs(va - vb);
          const diffBadge = diffVal >= 5 ? `<span style="font-size:10px;color:var(--text3);margin-left:2px">+${diffVal}</span>` : '';
          html += `<div class="compare-row">
        <div class="compare-cell ${aWin ? 'best' : vb > va ? 'worst' : ''}">${r.va || '—'}${aWin ? diffBadge : ''}</div>
        <div class="compare-stat-name">${r.l}</div>
        <div class="compare-cell ${bWin ? 'best' : va > vb ? 'worst' : ''}">${r.vb || '—'}${bWin ? diffBadge : ''}</div>
      </div>`;
        });
        html += '</div>';
      });

      // Playstyles
      html += `<div class="compare-table-section"><div class="compare-table-title">Play Styles</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:8px 0">
      <div style="display:flex;flex-wrap:wrap;gap:4px">${(a.playstyles || []).map(ps => `<span class="playstyle-chip ${ps.endsWith('+') ? 'plus' : ''}" style="font-size:10px;padding:3px 7px">${ps}</span>`).join('')}</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px">${(b.playstyles || []).map(ps => `<span class="playstyle-chip ${ps.endsWith('+') ? 'plus' : ''}" style="font-size:10px;padding:3px 7px">${ps}</span>`).join('')}</div>
    </div>
  </div>`;

      table.innerHTML = html;
    }

    function compareFromFavorites() {
      const favPlayers = favorites.slice(0, 2).map(id => allPlayers.find(p => p.id === id)).filter(Boolean);
      compareSlots[0] = favPlayers[0] || null;
      compareSlots[1] = favPlayers[1] || null;
      showPage('compare');
      renderCompareSlots();
      renderCompareTable();
    }

    // ════════════════════════════════════════════════════════
    // INIT
    // ════════════════════════════════════════════════════════
    renderCompareSlots();
    loadData();
