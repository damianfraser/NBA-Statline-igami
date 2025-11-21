from nba_api.stats.endpoints import ScoreboardV2, BoxScoreTraditionalV2
from datetime import datetime

def get_game_ids_for_date(date_str):
    sb = ScoreboardV2(game_date=date_str)
    games = sb.get_normalized_dict()["GameHeader"]
    return [(g["GAME_ID"], date_str) for g in games]

def get_boxscore_players(game_id):
    box = BoxScoreTraditionalV2(game_id=game_id)
    return box.get_normalized_dict()["PlayerStats"]
