import sqlite3
from .entities import RedditThread
from .config import DatabaseConfig

class Database:
    def __init__(self, config: DatabaseConfig):
        if config is None:
            raise ValueError('Missing database config')

        if config.database_name is None:
            raise ValueError('Missing database name')

        self.database_name = config.database_name
        self.__init_tables()

    def create_reddit_thread(self, reddit_thread: RedditThread) -> RedditThread:
        sql = """
            INSERT INTO reddit_thread(cfl_game_id, pregame_thread_id, game_thread_id, postgame_thread_id) 
            VALUES (:cfl_game_id, :pregame_thread_id, :game_thread_id, :postgame_thread_id)
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, {
            "cfl_game_id": reddit_thread.cfl_game_id,
            "pregame_thread_id": reddit_thread.pregame_thread_id, 
            "game_thread_id": reddit_thread.game_thread_id,
            "postgame_thread_id": reddit_thread.postgame_thread_id,
        })
        conn.commit()
        return reddit_thread
    
    def update_reddit_thread(self, reddit_thread: RedditThread) -> RedditThread:
        sql = """
            UPDATE reddit_thread
            SET pregame_thread_id = :pregame_thread_id,
                game_thread_id = :game_thread_id,
                postgame_thread_id = :postgame_thread_id
            WHERE cfl_game_id = :cfl_game_id
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, {
            "cfl_game_id": reddit_thread.cfl_game_id,
            "pregame_thread_id": reddit_thread.pregame_thread_id, 
            "game_thread_id": reddit_thread.game_thread_id,
            "postgame_thread_id": reddit_thread.postgame_thread_id,
        })
        conn.commit()
        return reddit_thread

    def find_reddit_thread(self, cfl_game_id: str) -> RedditThread:
        sql = """
            SELECT * 
            FROM reddit_thread
            WHERE cfl_game_id = :cfl_game_id
        """
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, {
            "cfl_game_id": cfl_game_id
        })
        result = res.fetchone()
        if result is None:
            return None

        thread = RedditThread(cfl_game_id)
        thread.pregame_thread_id = result[1]
        thread.game_thread_id = result[2]
        thread.postgame_thread_id = result[3]
        return thread

    def __get_connection(self): 
        return sqlite3.connect(f'./data/{self.database_name}.db')

    def __init_tables(self):
        cur = self.__get_connection().cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS reddit_thread(cfl_game_id, pregame_thread_id, game_thread_id, postgame_thread_id)")
