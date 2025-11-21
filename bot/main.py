from datetime import date
from bot.db import init_db, get_db, process_statline
from bot.nba_api_helpers import get_game_ids_for_date, get_boxscore_players
from bot.twitter import post_tweet
from bot.formatter import format_tweet

# Tweet only if:
# - it's a Statline-gami (first time ever), OR
# - it has happened fewer than this many times before
RARE_THRESHOLD = 5

def run():
    init_db()
    conn = get_db()

    today = date.today().strftime("%Y-%m-%d")
    games = get_game_ids_for_date(today)

    for game_id, game_date in games:
        players = get_boxscore_players(game_id)

        for p in players:
            result = process_statline(conn, game_id, game_date, p)

            if result["kind"] == "unique":
                should_tweet = True
            else:
                should_tweet = result["count_before"] < RARE_THRESHOLD

            if not should_tweet:
                continue

            tweet = format_tweet(result)
            post_tweet(tweet)

    conn.close()

if __name__ == "__main__":
    run()
