"""
Postgres management
"""
import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# logging
logger = logging
logger.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                   datefmt='%Y-%m-%d %H:%M',
                   level='DEBUG')

class DatabaseManager:
    """Database management"""
    def __init__(self, host, user, password, db_name, table_name):
        """Init."""
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.table_name = table_name

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host
            )
            return conn
        except Exception as err:
            logger.error(f"Error connecting to database: {err}")
            return None

    def create_table(self):
        """Create the table if it doesn't exist."""
        try:
            conn = self.connect()
            if conn is None:
                return

            cursor = conn.cursor()
            cursor.execute(sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    birthday DATE NOT NULL
                )
            """).format(sql.Identifier(self.table_name)))

            conn.commit()
            logger.info(f"Table '{self.table_name}' created successfully.")

            cursor.close()
            conn.close()
        except Exception as err:
            logger.error(f"Error creating table: {err}")

    def write_data(self, username, birthday):
        """Write data to the table."""
        try:
            conn = self.connect()
            if conn is None:
                return

            cursor = conn.cursor()
            cursor.execute(sql.SQL("""
                INSERT INTO {} (username, birthday) VALUES (%s, %s)
                ON CONFLICT (username) DO UPDATE SET birthday = EXCLUDED.birthday
            """).format(sql.Identifier(self.table_name)), (username, birthday))

            conn.commit()
            logger.info(f"Data inserted/updated in table '{self.table_name}' successfully.")

            cursor.close()
            conn.close()
        except Exception as err:
            logger.error(f"Error writing data to table: {err}")

    def get_data(self, username):
        """Retrieve data from the table."""
        try:
            conn = self.connect()
            if conn is None:
                return None

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(sql.SQL("SELECT * FROM {} WHERE username = %s").format(
                sql.Identifier(self.table_name)
            ), [username])
            data = cursor.fetchone()

            cursor.close()
            conn.close()
            logger.info(f"Data retrieved from table '{self.table_name}' successfully.")
            return data
        except Exception as err:
            logger.error(f"Error retrieving data from table: {err}")
            return None
