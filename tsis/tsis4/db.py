import psycopg2
from datetime import datetime

DB = "host='localhost' dbname='postgres' user='postgres' password='1234' port=5432"

def connect():
    conn = psycopg2.connect(DB)
    return conn

def create_table():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
        );

        CREATE TABLE game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
        );""")
        conn.commit()

def result(username, score, level):
    date=datetime.strf(datetime.now(), "%Y-%M-%d")
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO player(username) VALUES (%s)", (username,))
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]
        cur.execute("INSERT INTO game_sessions(player_id, score, level_reached, played_at) VALUES (%s, %s, %s, %s)", (player_id, score, level, date))
        conn.commit()

def leaderboard(limit = 10):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at 
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC, gs.played_at DESC
            LIMIT %s
        """, (limit, ))
        return cur.fetchall()
    
def pb(username):
    conn = connect()
    try:
        cur = conn.cursor()
        query = """
            SELECT MAX(gs.score) 
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            WHERE p.username = %s
        """
        cur.execute(query, (username,))
        result = cur.fetchone()[0]
        return result if result is not None else 0
    except Exception as e:
        print(f"Error fetching personal best: {e}")
        return 0
    finally:
        cur.close()
        conn.close()
        