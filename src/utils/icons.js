import clubs from "@/data/clubs.json";
import leagues from "@/data/leagues.json";
import playstyles from "@/data/ea_playstyles.json";
import playstylesPlusData from "@/data/ea_playstyles_plus.json";

/**
 * Convertit un nom de playstyle vers un slug de fichier
 * Exemple: "Tir Rasant" -> "tir-rasant"
 */
function playstyleNameToFilename(playstyleName) {
  if (!playstyleName) return "";
  return playstyleName
    .toLowerCase()
    .replace(/[\s']/g, "-")
    .replace(/--+/g, "-")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

/**
 * Récupère l'icône d'un club
 * @param {string} clubName - Nom du club
 * @returns {string|null} - Chemin de l'icône ou null
 */
export function getClubIcon(clubName) {
  if (!clubName || clubName === "Unknown") return null;
  const club = clubs?.find?.(
    (c) => c.name.toLowerCase() === clubName.toLowerCase()
  );
  return club?.icon ?? null;
}

/**
 * Récupère l'icône d'une ligue
 * @param {string} leagueName - Nom de la ligue
 * @returns {string|null} - Chemin de l'icône ou null
 */
export function getLeagueIcon(leagueName) {
  if (!leagueName || leagueName === "Unknown") return null;
  const league = leagues?.find?.(
    (l) => l.name.toLowerCase() === leagueName.toLowerCase()
  );
  return league?.icon ?? null;
}

/**
 * Récupère l'icône d'un playstyle (non-plus)
 * @param {string} playstyleName - Nom du playstyle
 * @returns {string|null} - Chemin local de l'icône ou null
 */
export function getPlaystyleIcon(playstyleName) {
  if (!playstyleName || playstyleName.endsWith("+")) return null;

  const filename = playstyleNameToFilename(playstyleName);
  if (!filename) return null;

  // Essayer d'abord le fichier exact
  return `/assets/playstyles/${filename}.png`;
}

/**
 * Récupère l'icône d'un playstyle+
 * @param {string} playstyleName - Nom du playstyle+
 * @returns {string|null} - Chemin local de l'icône ou null
 */
export function getPlaystylePlusIcon(playstyleName) {
  if (!playstyleName || !playstyleName.endsWith("+")) return null;

  // Retirer le '+' avant de traiter
  const baseName = playstyleName.slice(0, -1);
  const filename = playstyleNameToFilename(baseName);
  if (!filename) return null;

  return `/assets/playstyles_plus/${filename}.png`;
}

/**
 * Récupère l'icône d'un playstyle (détecte automatiquement + ou non)
 * @param {string} playstyleName - Nom du playstyle
 * @returns {string|null} - Chemin de l'icône ou null
 */
export function getPlaystyleIconAuto(playstyleName) {
  if (!playstyleName) return null;

  if (playstyleName.endsWith("+")) {
    return getPlaystylePlusIcon(playstyleName);
  }
  return getPlaystyleIcon(playstyleName);
}

/**
 * Récupère les données complètes d'un playstyle
 * @param {string} playstyleName - Nom du playstyle
 * @returns {object|null} - Données du playstyle ou null
 */
export function getPlaystyleData(playstyleName) {
  if (!playstyleName) return null;

  if (playstyleName.endsWith("+")) {
    return playstylesPlusData?.find?.(
      (p) => p.label.toLowerCase() === playstyleName.toLowerCase()
    ) ?? null;
  }

  return playstyles?.find?.(
    (p) => p.label.toLowerCase() === playstyleName.toLowerCase()
  ) ?? null;
}
