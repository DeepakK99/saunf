import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
from app.config import settings


class MySQLDB:
    """
    MySQL helper using connection pooling.
    Safe to use inside Celery workers and FastAPI routes.
    """

    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mysql_pool",
            pool_size=5,     # increase for heavy load
            pool_reset_session=True,
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DB,
        )

    @contextmanager
    def get_conn(self):
        """
        Gives you a connection + cursor using a 'with' block.
        Ensures commit/rollback/close are handled safely.
        """
        conn = None
        cursor = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)  # returns rows as dict
            yield cursor
            conn.commit()   # commit automatically
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def execute(self, query: str, params=None):
        """Run INSERT/UPDATE/DELETE and return affected rows."""
        with self.get_conn() as cur:
            cur.execute(query, params or ())
            return cur.rowcount

    def fetch_one(self, query: str, params=None):
        """Run SELECT and return a single row."""
        with self.get_conn() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()

    def fetch_all(self, query: str, params=None):
        """Run SELECT and return all rows."""
        with self.get_conn() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()


# create global DB instance
db = MySQLDB()
