// Script d'enrichissement des icônes
let clubsData = {};
let liguesData = {};
let playstyleData = {};
let playstylePlusData = {};

async function loadIconsData() {
  try {
    const [c, l, p, pp] = await Promise.all([
      fetch('src/data/clubs.json').then(r => r.json()),
      fetch('src/data/leagues.json').then(r => r.json()),
      fetch('src/data/ea_playstyles.json').then(r => r.json()),
      fetch('src/data/ea_playstyles_plus.json').then(r => r.json())
    ]);
    clubsData = c.reduce((acc, x) => { acc[x.nom] = x; return acc; }, {});
    liguesData = l.reduce((acc, x) => { acc[x.nom] = x; return acc; }, {});
    playstyleData = p.reduce((acc, x) => { acc[x.nom] = x; return acc; }, {});
    playstylePlusData = pp.reduce((acc, x) => { acc[x.nom] = x; return acc; }, {});
    console.log('✅ Icônes chargées:', Object.keys(clubsData).length, 'clubs,', Object.keys(liguesData).length, 'ligues');
  } catch(e) {
    console.warn('⚠️ Impossible de charger les icônes:', e);
  }
}

function getClubIcon(clubName) {
  if (!clubName) return null;
  const club = clubsData[clubName];
  if (!club || !club.local_path) return null;
  let path = club.local_path.replace('local_files/club_icons/', '/public/assets/clubs/');
  return path.endsWith('.png') ? path : path + '.png';
}

function getLeagueIcon(leagueName) {
  if (!leagueName) return null;
  const ligue = liguesData[leagueName];
  if (!ligue || !ligue.local_path) return null;
  let path = ligue.local_path.replace('local_files/league_icons/', '/public/assets/leagues/');
  return path.endsWith('.png') ? path : path + '.png';
}

function playstyleNameToFilename(name) {
  if (!name) return '';
  return name
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '');
}

function getPlaystyleIcon(psName) {
  if (!psName) return null;
  const isPlus = psName.endsWith('+');
  const cleanName = isPlus ? psName.slice(0, -1) : psName;
  const filename = playstyleNameToFilename(cleanName) + '.png';
  return isPlus ? `/public/assets/playstyles_plus/${filename}` : `/public/assets/playstyles/${filename}`;
}

// Patcher buildPlayerRowHTML pour ajouter les icônes
const originalBuildPlayerRowHTML = window.buildPlayerRowHTML;
window.buildPlayerRowHTML = function(p) {
  const rareteBg = p.rarete === 'Or Rare' ? 'linear-gradient(160deg,#3d2e0a,#c8a84b,#3d2e0a)' :
    p.rarete === 'Argent Rare' ? 'linear-gradient(160deg,#1a1a22,#8a8aa0,#1a1a22)' :
      'linear-gradient(160deg,#2a1a0a,#a06030,#2a1a0a)';

  const noteColor = p.rarete === 'Or Rare' ? 'var(--gold2)' : p.rarete === 'Argent Rare' ? '#b8b8c8' : '#c87840';

  const statsKeys = ['vitesse', 'tir', 'passes', 'dribble', 'defense', 'physique'];
  const statsLabels = ['VIT', 'TIR', 'PAS', 'DRI', 'DEF', 'PHY'];
  const statsHtml = statsKeys.map((k, i) => {
    const v = p.stats?.[k] || '—';
    const col = (typeof v === 'number')
      ? (v >= 85 ? '#22c55e' : v >= 75 ? '#86efac' : v >= 65 ? '#f0cc70' : v >= 55 ? '#f97316' : '#ef4444')
      : 'var(--text3)';
    return `<div class="stat-mini"><span class="stat-mini-val" style="color:${col}">${v}</span><span class="stat-mini-lbl">${statsLabels[i]}</span></div>`;
  }).join('');

  // Icônes
  const clubIcon = getClubIcon(p.club);
  const leagueIcon = getLeagueIcon(p.ligue);
  const playstyleIcons = (p.playstyles || []).slice(0, 3).map(ps => `<img src="${getPlaystyleIcon(ps)}" alt="${ps}" style="width:16px;height:16px;border-radius:2px" title="${ps}" onerror="this.style.display='none'">`);

  const clubBadge = clubIcon ? `<img src="${clubIcon}" alt="${p.club}" style="width:18px;height:18px;border-radius:50%;object-fit:cover" title="${p.club}" onerror="this.style.display='none'">` : `<span style="font-size:10px;color:var(--text3)">${p.club || '—'}</span>`;
  const leagueBadge = leagueIcon ? `<img src="${leagueIcon}" alt="${p.ligue}" style="width:18px;height:18px;border-radius:2px;object-fit:cover" title="${p.ligue}" onerror="this.style.display='none'">` : `<span style="font-size:10px;color:var(--text3)">${p.ligue || '—'}</span>`;

  const cardBg = p.rarete === 'Or Rare' ? 'linear-gradient(160deg,#3d2e0a,#c8a84b,#3d2e0a)' :
    p.rarete === 'Argent Rare' ? 'linear-gradient(160deg,#1a1a22,#8a8aa0,#1a1a22)' :
      'linear-gradient(160deg,#2a1a0a,#a06030,#2a1a0a)';

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
      <div class="player-meta" style="gap:6px;display:flex;align-items:center;flex-wrap:wrap">
        <span class="player-poste">${p.poste}</span>
        <span style="display:flex;gap:4px;align-items:center">${clubBadge}</span>
        <span style="display:flex;gap:4px;align-items:center">${leagueBadge}</span>
        ${playstyleIcons.length ? `<span style="display:flex;gap:3px">${playstyleIcons.join('')}</span>` : ''}
      </div>
      <div class="player-stats-mini">${statsHtml}</div>
    </div>
    <div class="player-right-col">
      <span class="player-ovr" style="color:${noteColor}">${p.note}</span>
      <div class="player-rarete-dot" style="background:${rareteBg};box-shadow:0 0 6px ${rareteBg}" title="${p.rarete}"></div>
    </div>`;
};
