import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <main style={{ backgroundColor: "#121212", minHeight: "100vh", padding: "3rem 2rem" }}>
      <header style={{ maxWidth: "1200px", margin: "0 auto 3rem auto", textAlign: "center" }}>
        <h1
          style={{
            fontSize: "4rem",
            color: "#ffffff",
            fontWeight: "900",
            letterSpacing: "-1.5px",
            margin: "0 0 1rem 0",
            fontFamily: "'Inter', sans-serif",
          }}
        >
          FC <span style={{ color: "#bb86fc" }}>Pulse</span>
        </h1>
        <p
          style={{
            color: "#a0a0a0",
            fontSize: "1.2rem",
            maxWidth: "600px",
            margin: "0 auto",
            lineHeight: "1.6",
          }}
        >
          Explorez les meilleures données EA Sports FC 26: Joueurs, Campagnes, Playstyles et plus.
        </p>
      </header>

      <div style={{ maxWidth: "1200px", margin: "0 auto", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "2rem" }}>
        {/* Carte Campagnes */}
        <Link
          to="/campaigns"
          style={{
            background: "linear-gradient(135deg, rgba(187, 134, 252, 0.1), rgba(3, 218, 198, 0.05))",
            border: "1px solid rgba(187, 134, 252, 0.3)",
            borderRadius: "16px",
            padding: "2rem",
            textDecoration: "none",
            color: "#fff",
            transition: "all 0.3s ease",
            cursor: "pointer",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = "rgba(187, 134, 252, 0.8)";
            e.currentTarget.style.transform = "translateY(-4px)";
            e.currentTarget.style.boxShadow = "0 10px 30px rgba(187, 134, 252, 0.2)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = "rgba(187, 134, 252, 0.3)";
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          <h2 style={{ margin: "0 0 1rem 0", fontSize: "1.8rem", fontWeight: "700" }}>
            🔥 Campagnes
          </h2>
          <p style={{ margin: 0, color: "#a0a0a0", lineHeight: "1.6" }}>
            Découvrez toutes les campagnes, équipes d'élite et événements spéciaux avec les joueurs recommandés.
          </p>
        </Link>

        {/* Carte Joueurs */}
        <div
          style={{
            background: "linear-gradient(135deg, rgba(3, 218, 198, 0.1), rgba(187, 134, 252, 0.05))",
            border: "1px solid rgba(3, 218, 198, 0.3)",
            borderRadius: "16px",
            padding: "2rem",
            opacity: 0.7,
          }}
        >
          <h2 style={{ margin: "0 0 1rem 0", fontSize: "1.8rem", fontWeight: "700" }}>
            ⚽ Joueurs
          </h2>
          <p style={{ margin: 0, color: "#a0a0a0", lineHeight: "1.6" }}>
            Bientôt disponible: Recherchez et comparez tous les joueurs avec leurs stats détaillées.
          </p>
        </div>

        {/* Carte Équipes */}
        <div
          style={{
            background: "linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(3, 218, 198, 0.05))",
            border: "1px solid rgba(0, 212, 255, 0.3)",
            borderRadius: "16px",
            padding: "2rem",
            opacity: 0.7,
          }}
        >
          <h2 style={{ margin: "0 0 1rem 0", fontSize: "1.8rem", fontWeight: "700" }}>
            👥 Équipes
          </h2>
          <p style={{ margin: 0, color: "#a0a0a0", lineHeight: "1.6" }}>
            Bientôt disponible: Construisez et optimisez vos équipes avec les meilleures syner gies.
          </p>
        </div>
      </div>

      {/* Info box */}
      <div
        style={{
          maxWidth: "1200px",
          margin: "4rem auto 0",
          background: "rgba(187, 134, 252, 0.05)",
          border: "1px solid rgba(187, 134, 252, 0.2)",
          borderRadius: "12px",
          padding: "2rem",
          color: "#a0a0a0",
        }}
      >
        <h3 style={{ margin: "0 0 1rem 0", color: "#fff" }}>ℹ️ À propos de FC Pulse</h3>
        <p style={{ margin: 0, lineHeight: "1.8" }}>
          FC Pulse est une plateforme complète dédiée à EA Sports FC 26. Nous agrégeons,
          enrichissons et visualisons les données des joueurs, campagnes, playstyles et bien
          d'autres informations pour vous aider à optimiser votre expérience de jeu.
        </p>
      </div>
    </main>
  );
}
