import requests

# APIs (free key "3")
players_url = "https://www.thesportsdb.com/api/v1/json/3/searchplayers.php"
honours_url = "https://www.thesportsdb.com/api/v1/json/3/lookuphonours.php"

def fetch_player_name(playername):
    params = {'p': playername}
    r = requests.get(players_url, params=params, timeout=10)
    if r.status_code == 200:
        data = r.json()
    exact_player_name = data["player"][0]['strPlayer']
    exact_player_id   = data["player"][0]['idPlayer']
    return exact_player_name, exact_player_id

def fetch_player_trophies(player_id):
    params = {"id": player_id}
    r = requests.get(honours_url, params=params, timeout=10)
    if r.status_code == 200:
        data = r.json()

        exact_honours = []
        for item in data["honours"]:
            exact_honours.append(item['strHonour'])

        counting_trophies = {}
        for honour in exact_honours:
            if honour in counting_trophies:
                counting_trophies[honour] += 1
            else:
                counting_trophies[honour] = 1
        return counting_trophies

def score_honours(counting_trophies):
    # very simple scoring: base 1 point per trophy
    # plus small bonuses for “bigger” ones (keyword match, case-insensitive)
    bonuses = [
        ("world cup", 8),
        ("uefa euro", 6),
        ("copa america", 6),
        ("champions league", 5),
        ("copa libertadores", 5),
        ("olympic", 4),
        ("league", 3),        # domestic leagues
        ("super cup", 2),
        ("cup", 2),           # domestic cups
        ("ballon", 6),        # individual
        ("best", 3),          # FIFA The Best / best player awards
        ("golden shoe", 4),
        ("team of the year", 2),
        ("world player", 4),
    ]

    total_titles = 0
    score = 0

    for honour, cnt in counting_trophies.items():
        total_titles += cnt
        score += cnt  # base points
        h = honour.lower()
        for key, bonus in bonuses:
            if key in h:
                score += bonus * cnt
                break  # apply first matching bonus only (keeps it simple)

    return total_titles, score

# ---------- main ----------
name1 = input("Enter Player 1: ")
p1_name, p1_id = fetch_player_name(name1)
p1_trophies = fetch_player_trophies(p1_id)
p1_total, p1_score = score_honours(p1_trophies)

name2 = input("Enter Player 2: ")
p2_name, p2_id = fetch_player_name(name2)
p2_trophies = fetch_player_trophies(p2_id)
p2_total, p2_score = score_honours(p2_trophies)

print("\n=== Results ===")
print(p1_name)
for h in sorted(p1_trophies, key=p1_trophies.get, reverse=True):
    print(h, p1_trophies[h])
print("TOTAL TITLES:", p1_total, " | SCORE:", p1_score)

print("\n" + p2_name)
for h in sorted(p2_trophies, key=p2_trophies.get, reverse=True):
    print(h, p2_trophies[h])
print("TOTAL TITLES:", p2_total, " | SCORE:", p2_score)

print("\n=== Verdict ===")
if p1_score > p2_score:
    print(p1_name, "wins")
elif p2_score > p1_score:
    print(p2_name, "wins")
else:
    print("Tie")
