import CampaignsList from "@/components/CampaignsList";

export default function CampaignsPage() {
  return (
    <main style={{ backgroundColor: "#121212", minHeight: "100vh", padding: "3rem 2rem" }}>
      <header style={{ maxWidth: "1200px", margin: "0 auto 3rem auto", textAlign: "center" }}>
        <h1 style={{ 
          fontSize: "4rem", 
          color: "#ffffff", 
          fontWeight: "900",
          letterSpacing: "-1.5px",
          margin: "0 0 1rem 0",
          fontFamily: "'Inter', sans-serif"
        }}>
          Campagnes <span style={{ color: "#bb86fc" }}>EA FC</span>
        </h1>
        <p style={{ color: "#a0a0a0", fontSize: "1.2rem", maxWidth: "600px", margin: "0 auto", lineHeight: "1.6" }}>
          L'historique complet et détaillé des événements et promotions spéciales récupéré par notre pipeline de données.
        </p>
      </header>
      
      <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
        <CampaignsList />
      </div>
    </main>
  );
}
