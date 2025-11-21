import sqlite3

DB_PATH = "data/nba_scorigami.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS statline_occurrences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        game_date TEXT,
        player_id TEXT,
        player_name TEXT,
        team TEXT,
        pts INTEGER,
        reb INTEGER,
        ast INTEGER,
        blk INTEGER,
        stl INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS statline_summary (
        pts INTEGER,
        reb INTEGER,
        ast INTEGER,
        blk INTEGER,
        stl INTEGER,
        count INTEGER NOT NULL,
        first_game_id TEXT,
        first_player_id TEXT,
        first_player_name TEXT,
        first_date TEXT,
        last_game_id TEXT,
        last_player_id TEXT,
        last_player_name TEXT,
        last_date TEXT,
        PRIMARY KEY (pts, reb, ast, blk, stl)
    );
    """)

    conn.commit()
    conn.close()


def process_statline(conn, game_id, game_date, p):
    pts = p["PTS"]
    reb = p["REB"]
    ast = p["AST"]
    blk = p["BLK"]
    stl = p["STL"]

    player_id = p["PLAYER_ID"]
    player_name = p["PLAYER_NAME"]
    team = p["TEAM_ABBREVIATION"]

    cur = conn.cursor()

    # Log occurrence
    cur.execute("""
        INSERT INTO statline_occurrences
        (game_id, game_date, player_id, player_name, team,
         pts, reb, ast, blk, stl)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (game_id, game_date, player_id, player_name, team,
          pts, reb, ast, blk, stl))

    # Lookup summary
    cur.execute("""
        SELECT * FROM statline_summary
        WHERE pts=? AND reb=? AND ast=? AND blk=? AND stl=?
    """, (pts, reb, ast, blk, stl))

    row = cur.fetchone()

    if row is None:
        # First time ever
        cur.execute("""
            INSERT INTO statline_summary
            (pts, reb, ast, blk, stl, count,
             first_game_id, first_player_id, first_player_name, first_date,
             last_game_id, last_player_id, last_player_name, last_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pts, reb, ast, blk, stl,
            1,
            game_id, player_id, player_name, game_date,
            game_id, player_id, player_name, game_date,
        ))

        conn.commit()

        return {
            "kind": "unique",
            "count_before": 0,
            "prior_player_name": None,
            "prior_date": None,
            "player_name": player_name,
            "team": team,
            "pts": pts, "reb": reb, "ast": ast, "blk": blk, "stl": stl,
            "game_date": game_date,
        }

    else:
        # Repeat
        prior_count = row["count"]
        prior_player = row["last_player_name"]
        prior_date = row["last_date"]

        cur.execute("""
            UPDATE statline_summary
            SET count=?,
                last_game_id=?,
                last_player_id=?,
                last_player_name=?,
                last_date=?
            WHERE pts=? AND reb=? AND ast=? AND blk=? AND stl=?
        """, (
            prior_count + 1,
            game_id, player_id, player_name, game_date,
            pts, reb, ast, blk, stl,
        ))

        conn.commit()

        return {
            "kind": "repeat",
            "count_before": prior_count,
            "prior_player_name": prior_player,
            "prior_date": prior_date,
            "player_name": player_name,
            "team": team,
            "pts": pts, "reb": reb, "ast": ast, "blk": blk, "stl": stl,
            "game_date": game_date,
        }
