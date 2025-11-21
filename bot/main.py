from datetime import datetime
import pytz

from bot.db import init_db, get_db, process_statline
from bot.nba_api_helpers import get_game_ids_for_date, get_boxscore_players
from bot.twitter import post_tweet
from bot.formatter import format_tweet

RARE_THRESHOLD = 5  # Tweet rare statlines


def run():
    init_db()
    conn = get_db()

    # NBA time (USA Eastern)
    eastern = pytz.timezone("US/Eastern")
    today = datetime.now(eastern).strftime("%Y-%m-%d")

    games = get_game_ids_for_date(today)

    for g in games:
        gid = g["game_id"]
        game_info = g


        players = get_boxscore_players(gid)

        for p in players:
            result = process_statline(conn, gid, g["date"], p)

            # Rare / igami filter
            if result["kind"] == "unique":
                should_tweet = True
            else:
                should_tweet = result["count_before"] < RARE_THRESHOLD


            if not should_tweet:
                continue

            tweet = format_tweet(result, game_info)

            post_tweet(tweet)

    conn.close()


if __name__ == "__main__":
    run()
