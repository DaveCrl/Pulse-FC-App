import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getClubIcon, getLeagueIcon, getPlaystyleIconAuto } from "@/utils/icons";

export default function PlayerDetailPage() {
  const { playerSlug } = useParams();
  const navigate = useNavigate();
  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedVersion, setSelectedVersion] = useState(0);

  useEffect(() => {
    loadPlayerData();
  }, [playerSlug]);

  async function loadPlayerData() {
    try {
      const response = await fetch("/src/data/players_clean.json");
      const players = await response.json();

      const foundPlayers = players.filter(
        (p) => (p.slug || p.nom?.toLowerCase().replace(/\s+/g, "-")) === playerSlug
      );

      if (foundPlayers.length > 0) {
        setPlayer(foundPlayers[0]);
        setSelectedVersion(0);
      } else {
        navigate("/");
      }
    } catch (error) {
      console.error("Erreur lors du chargement du joueur:", error);
      navigate("/");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "4rem", color: "#888" }}>
        Chargement...
      </div>
    );
  }

  if (!player) {
    return (
      <div style={{ textAlign: "center", padding: "4rem", color: "#888" }}>
        Joueur non trouvé.
      </div>
    );
  }

  const clubIcon = getClubIcon(player.club);
  const leagueIcon = getLeagueIcon(player.ligue);
  const playstyles = player.playstyles || [];

  const statKeys = [
    { key: "acceleration", label: "Accélération" },
    { key: "vitesse_pointe", label: "Vitesse Pointe" },
    { key: "finition", label: "Finition" },
    { key: "puissance_tir", label: "Puissance Tir" },
    { key: "tirs_loin", label: "Tirs Loin" },
    { key: "vista", label: "Vista" },
    { key: "passes_courtes", label: "Passes Courtes" },
    { key: "passes_longues", label: "Passes Longues" },
    { key: "dribbles", label: "Dribbles" },
    { key: "agilite", label: "Agilité" },
    { key: "equilibre", label: "Équilibre" },
    { key: "reactivite", label: "Réactivité" },
    { key: "controle_ballon", label: "Contrôle Balle" },
    { key: "interceptions", label: "Interceptions" },
    { key: "conscience_def", label: "Conscience Déf" },
    { key: "tacle_debout", label: "Tacle Debout" },
    { key: "detente", label: "Détente" },
    { key: "endurance", label: "Endurance" },
    { key: "force", label: "Force" },
  ];

  return (
    <main
      style={{
        backgroundColor: "#121212",
        minHeight: "100vh",
        padding: "3rem 2rem 6rem",
        maxWidth: "1400px",
        margin: "0 auto",
      }}
    >
      {/* Header avec retour */}
      <div style={{ marginBottom: "2rem", display: "flex", alignItems: "center", gap: "1rem" }}>
        <button
          onClick={() => navigate(-1)}
          style={{
            background: "rgba(255,255,255,0.1)",
            border: "none",
            color: "#fff",
            padding: "8px 16px",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "0.9rem",
            fontWeight: "600",
          }}
        >
          ← Retour
        </button>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 2fr",
          gap: "3rem",
          marginBottom: "3rem",
        }}
      >
        {/* Colonne gauche : Image + infos basiques */}
        <div>
          {player.image_carte ? (
            <img
              src={player.image_carte}
              alt={player.nom}
              style={{
                width: "100%",
                borderRadius: "16px",
                marginBottom: "1.5rem",
                border: "1px solid rgba(255,255,255,0.1)",
              }}
            />
          ) : (
            <div
              style={{
                width: "100%",
                aspectRatio: "3/4",
                backgroundColor: "#333",
                borderRadius: "16px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: "1.5rem",
                color: "#666",
              }}
            >
              Pas d'image
            </div>
          )}

          {/* Infos joueur */}
          <div style={{ background: "rgba(30, 30, 38, 0.4)", padding: "1.5rem", borderRadius: "12px" }}>
            <h2 style={{ margin: "0 0 1rem 0", fontSize: "1.8rem", fontWeight: "900" }}>
              {player.nom}
            </h2>

            <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
              {clubIcon && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <img src={clubIcon} alt={player.club} style={{ width: "24px", height: "24px" }} />
                  <small style={{ color: "#a0a0a0" }}>{player.club}</small>
                </div>
              )}
              {leagueIcon && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <img src={leagueIcon} alt={player.ligue} style={{ width: "24px", height: "24px" }} />
                  <small style={{ color: "#a0a0a0" }}>{player.ligue}</small>
                </div>
              )}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginBottom: "1rem" }}>
              <div>
                <small style={{ color: "#888" }}>POSTE</small>
                <div style={{ fontSize: "1.2rem", fontWeight: "700", color: "#bb86fc" }}>
                  {player.poste_fr}
                </div>
              </div>
              <div>
                <small style={{ color: "#888" }}>NOTE</small>
                <div style={{ fontSize: "1.2rem", fontWeight: "700", color: "#bb86fc" }}>
                  {player.note}
                </div>
              </div>
            </div>

            {/* Meta infos - Pied, Gestes Techniques, Playstyles */}
            <div style={{ color: "#888", fontSize: "0.85rem", lineHeight: "1.8", marginBottom: "1.5rem" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem" }}>
                <span style={{ color: "#bb86fc", fontWeight: "700" }}>Pied fort:</span>
                <span style={{ color: "#e8edf2" }}>{player.meta?.pied_fort}</span>
              </div>
              {player.meta?.pied_faible && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem" }}>
                  <span style={{ color: "#bb86fc", fontWeight: "700" }}>Mauvais pied:</span>
                  <span style={{ color: "#e8edf2" }}>{player.meta?.pied_faible}</span>
                </div>
              )}
              {player.meta?.gestes_techniques && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <span style={{ color: "#bb86fc", fontWeight: "700" }}>Gestes Techniques:</span>
                  <span style={{ color: "#e8edf2" }}>{player.meta?.gestes_techniques}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Colonne droite : Playstyles et infos détaillées */}
        <div>

          {/* Playstyles */}
          {playstyles.length > 0 && (
            <div
              style={{
                background: "rgba(30, 30, 38, 0.4)",
                padding: "2rem",
                borderRadius: "12px",
                marginBottom: "2rem",
              }}
            >
              <h3 style={{ margin: "0 0 1.5rem 0", fontSize: "1.2rem", fontWeight: "700" }}>
                🎮 Playstyles ({playstyles.length})
              </h3>
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "1rem",
                }}
              >
                {playstyles.map((ps, idx) => {
                  const psIcon = getPlaystyleIconAuto(ps);
                  return (
                    <div
                      key={idx}
                      style={{
                        background: "rgba(187, 134, 252, 0.1)",
                        padding: "0.75rem 1rem",
                        borderRadius: "8px",
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                      }}
                    >
                      {psIcon && (
                        <img
                          src={psIcon}
                          alt={ps}
                          style={{ width: "20px", height: "20px", objectFit: "contain" }}
                        />
                      )}
                      <span style={{ fontSize: "0.9rem", fontWeight: "600" }}>{ps}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Infos supplémentaires du joueur */}
          <div
            style={{
              background: "rgba(30, 30, 38, 0.4)",
              padding: "1.5rem",
              borderRadius: "12px",
              marginBottom: "2rem",
            }}
          >
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
              {player.meta?.age && (
                <div>
                  <small style={{ color: "#888" }}>ÂGE</small>
                  <div style={{ fontSize: "1.2rem", fontWeight: "700", color: "#bb86fc" }}>
                    {player.meta.age}
                  </div>
                </div>
              )}
              {player.meta?.taille_cm && (
                <div>
                  <small style={{ color: "#888" }}>TAILLE</small>
                  <div style={{ fontSize: "1.2rem", fontWeight: "700", color: "#bb86fc" }}>
                    {player.meta.taille_cm} cm
                  </div>
                </div>
              )}
              {player.meta?.poids_kg && (
                <div>
                  <small style={{ color: "#888" }}>POIDS</small>
                  <div style={{ fontSize: "1.2rem", fontWeight: "700", color: "#bb86fc" }}>
                    {player.meta.poids_kg} kg
                  </div>
                </div>
              )}
              {player.rarete && (
                <div>
                  <small style={{ color: "#888" }}>RARETE</small>
                  <div style={{ fontSize: "1.2rem", fontWeight: "700", color: player.rarete_couleur?.text || "#bb86fc" }}>
                    {player.rarete}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Séparation */}
      <hr style={{ borderColor: "rgba(255,255,255,0.1)", margin: "3rem 0" }} />

      {/* Stats détaillées */}
      {player.stats_detail && Object.keys(player.stats_detail).length > 0 && (
        <div
          style={{
            background: "rgba(30, 30, 38, 0.4)",
            padding: "2rem",
            borderRadius: "12px",
            marginBottom: "2rem",
          }}
        >
          <h3 style={{ margin: "0 0 1.5rem 0", fontSize: "1.2rem", fontWeight: "700" }}>
            📊 Stats Détaillées
          </h3>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
              gap: "1rem",
            }}
          >
            {statKeys.map(({ key, label }) => {
              const value = player.stats_detail?.[key];
              if (value === null || value === undefined) return null;
              return (
                <div
                  key={key}
                  style={{
                    background: "rgba(255,255,255,0.05)",
                    padding: "1rem",
                    borderRadius: "8px",
                  }}
                >
                  <small style={{ color: "#888" }}>{label}</small>
                  <div
                    style={{
                      fontSize: "1.2rem",
                      fontWeight: "700",
                      color: "#bb86fc",
                      marginTop: "0.25rem",
                    }}
                  >
                    {value}
                  </div>
                  {/* Barre de progression */}
                  <div
                    style={{
                      height: "4px",
                      background: "rgba(255,255,255,0.1)",
                      borderRadius: "2px",
                      marginTop: "0.5rem",
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        height: "100%",
                        width: `${(value / 99) * 100}%`,
                        background: "linear-gradient(90deg, #bb86fc, #03dac6)",
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </main>
  );
}
