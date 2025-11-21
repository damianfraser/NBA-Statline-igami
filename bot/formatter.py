from datetime import datetime

def pretty_date(d):
    dt = datetime.strptime(d, "%Y-%m-%d")
    return dt.strftime("%b %d, %Y")

def format_tweet(result):
    p = result["player_name"]
    t = result["team"]
    d = pretty_date(result["game_date"])
    pts = result["pts"]; reb = result["reb"]; ast = result["ast"]
    blk = result["blk"]; stl = result["stl"]

    line1 = f"{p}"
    line2 = f"{pts} PTS / {reb} REB / {ast} AST / {blk} BLK / {stl} STL\n"

    if result["kind"] == "unique":
        return (
            f"{line1}\n{line2}\n"
            f"NBA-Statline-gami! 🎉\n\n"
            f"This is the first time we've ever seen this exact line.\n"
            f"({d})"
        )
    else:
        prior = pretty_date(result["prior_date"])
        count = result["count_before"]
        return (
            f"{line1}\n{line2}\n"
            f"No NBA-Statline-gami.\n\n"
            f"That stat line has happened {count} "
            f"{'time' if count == 1 else 'times'} before,\n"
            f"most recently by {result['prior_player_name']} on {prior}.\n"
            f"({d}, {t})"
        )
