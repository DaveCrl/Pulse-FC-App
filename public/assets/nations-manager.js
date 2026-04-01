/**
 * Nations Manager - Utilitaires pour afficher les nations en français avec drapeaux
 */

let nationsTranslations = {};
let nationsMap = new Map();

/**
 * Charge les traductions et le mapping des nations
 */
async function loadNationsData() {
  try {
    const response = await fetch('public/data/nations_with_translations.json');
    const data = await response.json();
    
    data.forEach(nation => {
      nationsMap.set(nation.name_en, nation);
      nationsTranslations[nation.name_en] = nation.name_fr;
    });
    
    console.log('✅ Nations chargées:', nationsMap.size, 'nations');
    return true;
  } catch(e) {
    console.warn('⚠️ Impossible de charger les nations:', e);
    return false;
  }
}

/**
 * Obtient le nom français d'une nation
 * @param {string} englishName - Nom anglais de la nation
 * @returns {string} - Nom français ou nom anglais si non trouvé
 */
function getNationFrench(englishName) {
  return nationsTranslations[englishName] || englishName;
}

/**
 * Obtient les données complètes d'une nation
 * @param {string} englishName - Nom anglais de la nation
 * @returns {object} - Données de la nation
 */
function getNationData(englishName) {
  return nationsMap.get(englishName);
}

/**
 * Obtient l'URL du drapeau
 * @param {string} englishName - Nom anglais de la nation
 * @returns {string} - URL du drapeau
 */
function getNationFlag(englishName) {
  const nation = nationsMap.get(englishName);
  if (!nation) return null;
  return nation.flag_url;
}

/**
 * Crée un élément HTML pour afficher le drapeau d'une nation
 * @param {string} englishName - Nom anglais de la nation
 * @param {number} size - Taille du drapeau en pixels (default: 20)
 * @returns {string} - HTML du drapeau
 */
function getNationFlagHTML(englishName, size = 20) {
  const flagUrl = getNationFlag(englishName);
  const frenchName = getNationFrench(englishName);
  
  if (!flagUrl) {
    return `<span title="${frenchName}">${frenchName}</span>`;
  }
  
  return `<img 
    src="${flagUrl}" 
    alt="${frenchName}" 
    title="${frenchName}" 
    style="width:${size}px;height:${size}px;object-fit:contain;vertical-align:middle;margin-right:4px"
    onerror="this.style.display='none';this.nextSibling?.style.display='inline'"
  /><span style="display:none">${frenchName}</span>`;
}

/**
 * Crée un élément HTML pour afficher la nation avec drapeau et nom
 * @param {string} englishName - Nom anglais de la nation
 * @param {number} flagSize - Taille du drapeau en pixels
 * @returns {string} - HTML complet
 */
function getNationFullHTML(englishName, flagSize = 16) {
  const flagUrl = getNationFlag(englishName);
  const frenchName = getNationFrench(englishName);
  
  if (!flagUrl) {
    return `<span class="nation-badge">${frenchName}</span>`;
  }
  
  return `<div class="nation-badge" style="display:flex;align-items:center;gap:4px">
    <img 
      src="${flagUrl}" 
      alt="${frenchName}" 
      style="width:${flagSize}px;height:${flagSize}px;object-fit:contain"
      onerror="this.style.display='none'"
    />
    <span>${frenchName}</span>
  </div>`;
}

// Export pour les modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    loadNationsData,
    getNationFrench,
    getNationData,
    getNationFlag,
    getNationFlagHTML,
    getNationFullHTML
  };
}
