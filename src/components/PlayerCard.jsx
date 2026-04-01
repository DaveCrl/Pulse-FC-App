import { useState } from "react";
import { getClubIcon, getLeagueIcon, getPlaystyleIconAuto } from "@/utils/icons";

export default function PlayerCard({ player, onClick }) {
  const [imageError, setImageError] = useState(false);
  const clubIcon = getClubIcon(player.club);
  const leagueIcon = getLeagueIcon(player.league);
  const playstyles = player.playstyles || [];

  const handleClick = () => {
    if (onClick) onClick(player);
  };

  const handleImageError = () => {
    setImageError(true);
  };

  return (
    <div
      style={{
        background: "linear-gradient(145deg, #1e1e26, #121212)",
        borderRadius: "16px",
        overflow: "hidden",
        border: "1px solid rgba(255,255,255,0.05)",
        color: "#fff",
        transition: "transform 0.2s ease, box-shadow 0.2s ease",
        cursor: "pointer",
        display: "flex",
        flexDirection: "column",
        boxShadow: "0 4px 15px rgba(0,0,0,0.2)",
      }}
      onClick={handleClick}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-6px)";
        e.currentTarget.style.boxShadow = "0 10px 30px rgba(0,0,0,0.4)";
        e.currentTarget.style.border = "1px solid rgba(187,134,252,0.4)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "0 4px 15px rgba(0,0,0,0.2)";
        e.currentTarget.style.border = "1px solid rgba(255,255,255,0.05)";
      }}
    >
      {/* Image carte */}
      {!imageError && (player.image_carte || player.card_image) ? (
        <div style={{ position: "relative", width: "100%", aspectRatio: "3/4" }}>
          <img
            src={player.image_carte || player.card_image}
            alt={player.nom || player.player_name}
            style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
            loading="lazy"
            onError={handleImageError}
          />
        </div>
      ) : (
        <div
          style={{
            width: "100%",
            aspectRatio: "3/4",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "#333",
          }}
        >
          <span style={{ color: "#666", fontSize: "0.9rem" }}>No Image</span>
        </div>
      )}

      {/* Infos */}
      <div style={{ padding: "12px", display: "flex", flexDirection: "column", gap: "6px", flex: 1 }}>
        <strong
          style={{
            fontSize: "1.05rem",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {player.nom || player.player_name}
        </strong>

        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: "6px" }}>
            <span style={{ color: "#bb86fc", fontWeight: "900", fontSize: "1.15rem" }}>
              {player.note || player.rating}
            </span>
            <span style={{ fontSize: "0.85rem", color: "#a0a0a0", fontWeight: "600" }}>
              {player.poste_fr || player.position}
            </span>
          </div>

          <div style={{ display: "flex", gap: "6px" }}>
            {clubIcon && (
              <img
                src={clubIcon}
                alt={player.club}
                style={{ width: "20px", height: "20px", objectFit: "contain" }}
                title={player.club}
              />
            )}
            {leagueIcon && (
              <img
                src={leagueIcon}
                alt={player.league}
                style={{ width: "20px", height: "20px", objectFit: "contain" }}
                title={player.league}
              />
            )}
          </div>
        </div>

        {/* Rarete */}
        <div
          style={{
            fontSize: "0.75rem",
            color: "#888",
            marginTop: "2px",
            fontWeight: "500",
            letterSpacing: "0.3px",
          }}
        >
          {player.rarete || player.card_type}
        </div>

        {/* Playstyles icons */}
        {playstyles.length > 0 && (
          <div
            style={{
              display: "flex",
              gap: "4px",
              flexWrap: "wrap",
              marginTop: "6px",
              maxHeight: "30px",
              overflow: "hidden",
            }}
          >
            {playstyles.slice(0, 4).map((ps, idx) => {
              const psIcon = getPlaystyleIconAuto(ps);
              return psIcon ? (
                <img
                  key={idx}
                  src={psIcon}
                  alt={ps}
                  style={{ width: "18px", height: "18px", objectFit: "contain" }}
                  title={ps}
                />
              ) : null;
            })}
            {playstyles.length > 4 && (
              <span style={{ fontSize: "0.7rem", color: "#888", lineHeight: "18px" }}>
                +{playstyles.length - 4}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
