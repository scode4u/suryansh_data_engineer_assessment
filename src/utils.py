import os
import mysql.connector

# Path to schema.sql relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")


def get_connection():
    """
    Create a MySQL connection using Docker credentials.
    Defaults match docker-compose.initial.yml / final.yml.
    """
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3080")),
        user=os.getenv("MYSQL_USER", "db_user"),
        # user=os.getenv("MYSQL_USER", "root"),
        # password=os.getenv("MYSQL_PASSWORD", "6equj5_db_user"),
        password=os.getenv("MYSQL_PASSWORD", "babu"),
        database=os.getenv("MYSQL_DATABASE", "home_db"),
    )
    return conn


def init_db():
    """
    Run schema.sql against the MySQL database.
    This DROPs and CREATEs tables, so it is safe for reruns.
    """
    conn = get_connection()
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        sql = f.read()

    # Very simple split on ";"
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    for stmt in statements:
        cursor.execute(stmt)

    conn.commit()
    cursor.close()
    conn.close()
