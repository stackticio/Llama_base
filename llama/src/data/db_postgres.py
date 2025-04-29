import os
import psycopg2
from psycopg2 import sql, pool
import logging

logging.basicConfig(level=logging.INFO)

# PostgreSQL connection pool
postgres_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("POSTGRESS_HOST"),
    database=os.getenv("POSTGRESS_DATABASE_database"),
    user=os.getenv("POSTGRESS_USERNAME_database"),
    password=os.getenv("POSTGRESS_PASSWORD_database"),
    port=int(os.getenv("POSTGRESS_PORT", 5432))  # Default PostgreSQL port
)

def get_postgres_conn():
    """
    Get a connection from the pool.
    """
    try:
        return postgres_pool.getconn()
    except Exception as e:
        logging.error(f"Failed to get PostgreSQL connection: {str(e)}")
        raise RuntimeError("Could not connect to the PostgreSQL database.")

def release_postgres_conn(conn):
    """
    Return a connection back to the pool.
    """
    try:
        postgres_pool.putconn(conn)
    except Exception as e:
        logging.error(f"Failed to release PostgreSQL connection: {str(e)}")

def execute_sql(conn, query, params=None):
    """
    Execute a given SQL query using an existing connection.
    Parameters can be passed to safely format the query.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql.SQL(query), params or ())
        if cursor.description:  # If there is a result set
            results = cursor.fetchall()
            cursor.close()
            return results
        else:
            conn.commit()  # For INSERT/UPDATE/DELETE
            cursor.close()
            return None
    except Exception as e:
        conn.rollback()
        logging.error(f"Database query failed: {str(e)}")
        raise RuntimeError(f"Database query failed: {str(e)}")
