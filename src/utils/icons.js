import clubs from "@/data/clubs.json";
import leagues from "@/data/leagues.json";

export function getClubIcon(clubName) {
  if (!clubName) return null;
  const club = clubs.find(
    (c) => c.name.toLowerCase() === clubName.toLowerCase()
  );
  return club?.icon ?? null;
}

export function getLeagueIcon(leagueName) {
  if (!leagueName) return null;
  const league = leagues.find(
    (l) => l.name.toLowerCase() === leagueName.toLowerCase()
  );
  return league?.icon ?? null;
}
