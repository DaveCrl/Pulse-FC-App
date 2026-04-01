import json

def analyze_players():
    print("Loading players...")
    with open('players_clean.json', 'r', encoding='utf-8') as f:
        players = json.load(f)
    print(f"Total players: {len(players)}")

    names = {}
    raretes = {}
    for p in players:
        nom = p.get('nom', 'Unknown')
        names[nom] = names.get(nom, [])
        names[nom].append(p)
        
        rarete = p.get('rarete', 'Unknown')
        raretes[rarete] = raretes.get(rarete, 0) + 1

    multi_version = {k: v for k,v in names.items() if len(v) > 1}
    print(f"Players with multiple versions: {len(multi_version)}")

    # Print an example of a player with multiple versions
    if multi_version:
        example_name = list(multi_version.keys())[0]
        print(f"\nExample - {example_name}:")
        for p in multi_version[example_name]:
            print(f"- ID: {p.get('id')}, Rareté: {p.get('rarete')}, Note: {p.get('note')}")

    print("\nRarities count:")
    for k, v in sorted(raretes.items(), key=lambda item: item[1], reverse=True)[:10]:
        print(f"{k}: {v}")
        
    # Check what kind of IDs we have for similar players
    print("\nIDs for Mbappe:")
    mbappe = names.get('Kylian Mbappé', [])
    for p in mbappe:
         print(f"- ID: {p.get('id')}, Rareté: {p.get('rarete')}, Note: {p.get('note')}")

if __name__ == '__main__':
    analyze_players()
