import campaignsData from "@/data/campaigns_full.json";

export function getAllCampaigns() {
  return (campaignsData.campaigns || []).sort(
    (a, b) => new Date(b.date) - new Date(a.date)
  );
}

export function getCampaignBySlug(slug) {
  return (campaignsData.campaigns || []).find((c) => c.slug === slug) ?? null;
}
