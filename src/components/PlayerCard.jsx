import { getClubIcon, getLeagueIcon } from "@/utils/icons";

export default function PlayerCard({ player }) {
  const clubIcon = getClubIcon(player.club);
  const leagueIcon = getLeagueIcon(player.league);

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
      {player.card_image && player.card_image !== "N/A" ? (
        <div style={{ position: "relative", width: "100%", aspectRatio: "3/4" }}>
          <img
            src={player.card_image}
            alt={player.player_name}
            style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
            loading="lazy"
          />
        </div>
      ) : (
        <div style={{ width: "100%", aspectRatio: "3/4", display: "flex", alignItems: "center", justifyContent: "center", background: "#333" }}>
          <span style={{ color: "#666", fontSize: "0.9rem" }}>No Image</span>
        </div>
      )}

      {/* Infos */}
      <div style={{ padding: "12px", display: "flex", flexDirection: "column", gap: "6px" }}>
        <strong style={{ fontSize: "1.05rem", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
          {player.player_name}
        </strong>
        
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: "6px" }}>
            <span style={{ color: "#bb86fc", fontWeight: "900", fontSize: "1.15rem" }}>{player.rating}</span>
            <span style={{ fontSize: "0.85rem", color: "#a0a0a0", fontWeight: "600" }}>{player.position}</span>
          </div>

          <div style={{ display: "flex", gap: "6px" }}>
            {clubIcon && <img src={clubIcon} alt={player.club} style={{ width: "20px", height: "20px", objectFit: "contain" }} title={player.club} />}
            {leagueIcon && <img src={leagueIcon} alt={player.league} style={{ width: "20px", height: "20px", objectFit: "contain" }} title={player.league} />}
          </div>
        </div>
        
        <div style={{ fontSize: "0.75rem", color: "#888", marginTop: "2px", fontWeight: "500", letterSpacing: "0.3px" }}>
          {player.card_type}
        </div>
      </div>
    </div>
  );
}
