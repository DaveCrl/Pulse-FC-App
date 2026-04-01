import json

files = [
    "/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_clean.json",
    "/Users/dave-wilsoncarmel/Downloads/Pulse-FC-App-claude-audit-and-prompts-kpUy0/players_merged.json"
]

for filepath in files:
    with open(filepath) as f:
        players = json.load(f)
    
    count_tir_enroule = 0
    count_passe_fouettee = 0
    count_passe_fouettee_plus = 0
    
    for player in players:
        playstyles = player.get("playstyles", [])
        for i, ps in enumerate(playstyles):
            if ps in ["Tir Enroulé +", "Tir Enroulé+"]:
                playstyles[i] = "Tir en finesse +"
                count_tir_enroule += 1
            elif ps == "Passe Fouettée":
                playstyles[i] = "Passe travaillée"
                count_passe_fouettee += 1
            elif ps == "Passe Fouettée+":
                playstyles[i] = "Passe travaillée +"
                count_passe_fouettee_plus += 1
    
    with open(filepath, "w") as f:
        json.dump(players, f, ensure_ascii=False)
    
    print(f"✅ {filepath.split('/')[-1]}:")
    print(f"  - Tir Enroulé+ → Tir en finesse+: {count_tir_enroule}")
    print(f"  - Passe Fouettée → Passe travaillée: {count_passe_fouettee}")
    print(f"  - Passe Fouettée+ → Passe travaillée+: {count_passe_fouettee_plus}")
