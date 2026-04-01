import campaignsData from "@/data/campaigns_full.json";

// Cache pour éviter les recherchs multiples
let playersBaseCache = null;

/**
 * Charge et cache les données de joueurs de base
 */
async function loadPlayersBase() {
  if (playersBaseCache) return playersBaseCache;
  
  try {
    const response = await fetch("/players_clean.json");
    playersBaseCache = await response.json();
    return playersBaseCache;
  } catch (error) {
    console.error("Erreur lors du chargement de players_clean.json:", error);
    return [];
  }
}

/**
 * Normalize un nom de joueur pour le matching
 */
function normalizePlayerName(name) {
  if (!name) return "";
  return name
    .toLowerCase()
    .trim()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, ""); // Remove accents
}

/**
 * Enrichit les données d'un joueur de campagne avec les données de base
 */
async function enrichPlayerData(campaignPlayer) {
  if (campaignPlayer.club && campaignPlayer.club !== "Unknown") {
    return campaignPlayer; // Déjà enrichi
  }

  const playersBase = await loadPlayersBase();
  if (!playersBase || playersBase.length === 0) return campaignPlayer;

  const normalizedCampaignName = normalizePlayerName(campaignPlayer.player_name);

  // Chercher le joueur dans la base
  const matchedPlayer = playersBase.find((p) => {
    const normalizedBaseName = normalizePlayerName(p.nom || p.player_name);
    return normalizedBaseName === normalizedCampaignName;
  });

  if (matchedPlayer) {
    return {
      ...campaignPlayer,
      club: campaignPlayer.club !== "Unknown" ? campaignPlayer.club : matchedPlayer.club,
      league: campaignPlayer.league !== "Unknown" ? campaignPlayer.league : matchedPlayer.ligue,
      nation: campaignPlayer.nation !== "Unknown" ? campaignPlayer.nation : matchedPlayer.nationalite,
      playstyles: matchedPlayer.playstyles || [],
      image_carte:
        campaignPlayer.card_image && campaignPlayer.card_image !== "N/A"
          ? campaignPlayer.card_image
          : matchedPlayer.image_carte,
      stats: matchedPlayer.stats || {},
      stats_detail: matchedPlayer.stats_detail || {},
    };
  }

  return campaignPlayer;
}

/**
 * Enrichit tous les joueurs d'une campagne
 */
async function enrichCampaignData(campaign) {
  const enrichedPlayers = await Promise.all(
    campaign.players.map((p) => enrichPlayerData(p))
  );

  return {
    ...campaign,
    players: enrichedPlayers,
  };
}

/**
 * Récupère toutes les campagnes (enrichies si possible)
 */
export async function getAllCampaigns() {
  const campaigns = (campaignsData.campaigns || []).sort(
    (a, b) => new Date(b.date) - new Date(a.date)
  );

  // Enrichir les campagnes en parallèle
  return Promise.all(campaigns.map((c) => enrichCampaignData(c)));
}

/**
 * Récupère une campagne spécifique par slug
 */
export async function getCampaignBySlug(slug) {
  const campaign = (campaignsData.campaigns || []).find((c) => c.slug === slug) ?? null;
  if (!campaign) return null;

  return enrichCampaignData(campaign);
}

/**
 * Récupère toutes les campagnes en synchrone (sans enrichissement)
 * Utile pour des opérations rapides où l'enrichissement n'est pas nécessaire
 */
export function getAllCampaignsSync() {
  return (campaignsData.campaigns || []).sort(
    (a, b) => new Date(b.date) - new Date(a.date)
  );
}
