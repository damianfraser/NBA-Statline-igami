from nba_api.stats.endpoints import ScoreboardV2, BoxScoreTraditionalV2
from nba_api.stats.static import teams as static_teams

TEAM_LOOKUP = None  # team_id → {abbreviation, full_name}


def get_team_lookup():
    global TEAM_LOOKUP
    if TEAM_LOOKUP is None:
        TEAM_LOOKUP = {}
        all_teams = static_teams.get_teams()
        for t in all_teams:
            TEAM_LOOKUP[t["id"]] = {
                "abbr": t["abbreviation"],
                "name": t["full_name"]
            }
    return TEAM_LOOKUP


def get_game_ids_for_date(date_str: str):
    sb = ScoreboardV2(game_date=date_str)
    data = sb.get_normalized_dict()
    lookup = get_team_lookup()

    if not data["GameHeader"]:
        print("No games found for:", date_str)
        return []

    games = []
    for g in data["GameHeader"]:
        gid = g["GAME_ID"]
        home_id = g["HOME_TEAM_ID"]
        away_id = g["VISITOR_TEAM_ID"]

        home = lookup.get(home_id, {"abbr": "UNK", "name": "Unknown"})
        away = lookup.get(away_id, {"abbr": "UNK", "name": "Unknown"})

        # Box score summary includes scoring
        line = next((l for l in data["LineScore"] if l["TEAM_ID"] == home_id), None)
        home_pts = line["PTS"] if line else None

        line = next((l for l in data["LineScore"] if l["TEAM_ID"] == away_id), None)
        away_pts = line["PTS"] if line else None

        games.append({
            "game_id": gid,
            "date": date_str,
            "home_abbr": home["abbr"],
            "home_name": home["name"],
            "away_abbr": away["abbr"],
            "away_name": away["name"],
            "home_pts": home_pts,
            "away_pts": away_pts
        })

    return games


def get_boxscore_players(game_id: str):
    box = BoxScoreTraditionalV2(game_id=game_id)
    return box.get_normalized_dict()["PlayerStats"]
