import { useState } from "react";
import { getAllCampaigns } from "@/utils/campaigns";
import PlayerCard from "./PlayerCard";

export default function CampaignsList() {
  const campaigns = getAllCampaigns();
  const [activeFilter, setActiveFilter] = useState("all");

  const filteredCampaigns = activeFilter === "all" 
    ? campaigns 
    : campaigns.filter(c => c.slug === activeFilter);

  // Styles de navigation Premium
  const navStyle = {
    position: "sticky",
    top: "0",
    zIndex: 100,
    background: "rgba(18, 18, 18, 0.85)",
    backdropFilter: "blur(12px)",
    padding: "1rem 1rem",
    marginBottom: "2rem",
    borderBottom: "1px solid rgba(255,255,255,0.05)",
    display: "flex",
    gap: "12px",
    overflowX: "auto",
    scrollBehavior: "smooth",
    WebkitOverflowScrolling: "touch",
    scrollbarWidth: "none", // Pour Firefox
  };

  const cssHideScrollbar = `
    .sticky-nav::-webkit-scrollbar {
      display: none;
    }
  `;

  const btnStyle = (isActive) => ({
    background: isActive ? "linear-gradient(90deg, #bb86fc, #03dac6)" : "rgba(255,255,255,0.05)",
    color: isActive ? "#000" : "#fff",
    border: "1px solid",
    borderColor: isActive ? "transparent" : "rgba(255,255,255,0.1)",
    padding: "10px 20px",
    borderRadius: "24px",
    cursor: "pointer",
    fontWeight: "700",
    fontSize: "0.95rem",
    whiteSpace: "nowrap",
    transition: "all 0.2s ease",
    boxShadow: isActive ? "0 4px 15px rgba(187, 134, 252, 0.4)" : "none",
  });

  return (
    <div style={{ fontFamily: "'Inter', sans-serif" }}>
      <style>{cssHideScrollbar}</style>
      
      {/* Navigation Horizontale Sticky */}
      <div style={navStyle} className="sticky-nav">
        <button 
          style={btnStyle(activeFilter === "all")} 
          onClick={() => setActiveFilter("all")}
          onMouseEnter={(e) => { if(activeFilter !== "all") e.currentTarget.style.background = "rgba(255,255,255,0.1)"; }}
          onMouseLeave={(e) => { if(activeFilter !== "all") e.currentTarget.style.background = "rgba(255,255,255,0.05)"; }}
        >
          🔥 Dernières Campagnes
        </button>
        {campaigns.map(c => (
          <button 
            key={`nav-${c.slug}`}
            style={btnStyle(activeFilter === c.slug)}
            onClick={() => setActiveFilter(c.slug)}
            onMouseEnter={(e) => { if(activeFilter !== c.slug) e.currentTarget.style.background = "rgba(255,255,255,0.1)"; }}
            onMouseLeave={(e) => { if(activeFilter !== c.slug) e.currentTarget.style.background = "rgba(255,255,255,0.05)"; }}
          >
            {c.name}
          </button>
        ))}
      </div>

      <div style={{ padding: "0 1rem" }}>
        {filteredCampaigns.map((campaign) => (
          <section key={campaign.slug} id={campaign.slug} style={{ 
            marginBottom: "4rem", 
            padding: "2rem", 
            background: "rgba(30, 30, 38, 0.4)", 
            borderRadius: "24px", 
            border: "1px solid rgba(255, 255, 255, 0.05)" 
          }}>
            {/* Header campagne */}
            <div style={{ marginBottom: "24px", borderBottom: "1px solid rgba(255,255,255,0.1)", paddingBottom: "16px" }}>
              <h2 style={{ 
                margin: "0 0 8px 0", 
                fontSize: "2.2rem", 
                fontWeight: "900",
                color: "#fff", 
                background: "linear-gradient(90deg, #fff, #bb86fc)", 
                WebkitBackgroundClip: "text", 
                WebkitTextFillColor: "transparent",
                letterSpacing: "-0.5px"
              }}>
                {campaign.name}
              </h2>
              <div style={{ fontSize: "1rem", color: "#a0a0a0", display: "flex", gap: "1.5rem", fontWeight: "500" }}>
                <span>📅 {campaign.date}</span>
                <span>🎮 {campaign.players.length} joueurs édito</span>
              </div>
            </div>

            {/* Grid joueurs via PlayerCard */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
                gap: "20px",
              }}
            >
              {campaign.players.map((player, index) => (
                <PlayerCard
                  key={`${campaign.slug}-${player.player_name}-${index}`}
                  player={player}
                />
              ))}
            </div>
          </section>
        ))}
        
        {filteredCampaigns.length === 0 && (
          <div style={{ textAlign: "center", padding: "4rem", color: "#888" }}>
            Aucune campagne trouvée.
          </div>
        )}
      </div>
    </div>
  );
}
