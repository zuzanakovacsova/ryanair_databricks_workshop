import os
import time 
import streamlit as st
from psycopg_pool import ConnectionPool
from psycopg import sql

postgres_password = None
last_password_refresh = 0
connection_pool = None

def refresh_oauth_token(workspace_client):
    """Refresh OAuth token if expired."""
    global postgres_password, last_password_refresh
    if postgres_password is None or time.time() - last_password_refresh > 900:
        print("Refreshing PostgreSQL OAuth token")
        try:
            postgres_password = workspace_client.config.oauth_token().access_token
            last_password_refresh = time.time()
        except Exception as e:
            st.error(f"❌ Failed to refresh OAuth token: {str(e)}")
            st.stop()

def get_connection_pool(workspace_client):
    """Get or create the connection pool."""
    global connection_pool
    if connection_pool is None:
        refresh_oauth_token(workspace_client)
        conn_string = (
            f"dbname={os.getenv('PGDATABASE')} "
            f"user={os.getenv('PGUSER')} "
            f"password={postgres_password} "
            f"host={os.getenv('PGHOST')} "
            f"port={os.getenv('PGPORT')} "
            f"sslmode={os.getenv('PGSSLMODE', 'require')} "
            f"application_name={os.getenv('PGAPPNAME')}"
        )
        connection_pool = ConnectionPool(conn_string, min_size=2, max_size=10)
    return connection_pool

def get_connection(workspace_client):
    """Get a connection from the pool."""
    global connection_pool
    
    # Recreate pool if token expired
    if postgres_password is None or time.time() - last_password_refresh > 900:
        if connection_pool:
            connection_pool.close()
            connection_pool = None
    
    return get_connection_pool(workspace_client).connection()

def get_schema_name():
    """Get the schema name in the format {PGAPPNAME}_schema_{PGUSER}."""
    pgappname = os.getenv("PGAPPNAME", "my_app")
    pguser = os.getenv("PGUSER", "").replace('-', '')
    return f"{pgappname}_schema_{pguser}"

def init_database(workspace_client):
    """Initialize database schema and table."""
    with get_connection(workspace_client) as conn:
        with conn.cursor() as cur:
            schema_name = get_schema_name()
            
            cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name)))
            cur.execute(sql.SQL("""
                CREATE TABLE IF NOT EXISTS {}.request_history (
                    id SERIAL PRIMARY KEY,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """).format(sql.Identifier(schema_name)))
            conn.commit()
            return True
        
def add_request(prompt, response, workspace_client):
    with get_connection(workspace_client) as conn:
        with conn.cursor() as cur:
            schema = get_schema_name()
            cur.execute(sql.SQL("""
                    INSERT INTO {}.request_history (prompt, response) 
                    VALUES (%s, %s)
                """).format(sql.Identifier(schema)),
                (prompt.strip(), response.strip()) # <--- The data tuple
            )
            conn.commit()

def get_requests(workspace_client):
    with get_connection(workspace_client) as conn:
        with conn.cursor() as cur:
            schema = get_schema_name()
            cur.execute(sql.SQL("SELECT id, prompt, response, created_at FROM {}.request_history ORDER BY created_at DESC LIMIT 3").format(sql.Identifier(schema)))
            return cur.fetchall()