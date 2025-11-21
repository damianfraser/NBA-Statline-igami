from datetime import datetime

def pretty_date(d):
    dt = datetime.strptime(d, "%Y-%m-%d")
    return dt.strftime("%b %d, %Y")


def format_tweet(result, game_info):
    p = result["player_name"]
    t = result["team"]
    d = pretty_date(result["game_date"])

    pts = result["pts"]
    reb = result["reb"]
    ast = result["ast"]
    blk = result["blk"]
    stl = result["stl"]

    # Game info
    home_pts = game_info["home_pts"]
    away_pts = game_info["away_pts"]
    home_name = game_info["home_name"]
    away_name = game_info["away_name"]

    # Score line text
    score_line = f"{home_name} {home_pts} | {away_pts} {away_name}\nFinal\n"

    # Statline header
    header = f"{p}\n{pts} PTS / {reb} REB / {ast} AST / {blk} BLK / {stl} STL\n\n"

    if result["kind"] == "unique":
        return (
            header +
            score_line +
            "\nStatline-gami! 🎉\n\n"
            "This is the first time we've ever seen this exact line."
        )
    else:
        prior = pretty_date(result["prior_date"])
        count = result["count_before"]

        return (
            header +
            score_line +
            "\nRare statline.\n\n"
            f"That stat line has happened {count} "
            f"{'time' if count == 1 else 'times'} before,\n"
            f"most recently by {result['prior_player_name']} on {prior}.\n"
        )
