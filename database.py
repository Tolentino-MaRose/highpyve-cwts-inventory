import sqlite3
import os

DB = 'cwts_inventory.db'

def init_db():
    """ Initialize the SQLite database using schema.sql if the database file 
    does not exist."""
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            with open('schema.sql', 'r') as f:
                conn.executescript(f.read())

def query_db(query, args=(), one=False):
    """Execute any SQL query and return results (dicts for SELECT)."""
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute('PRAGMA foreign_keys = ON')
            cursor = conn.execute(query, args)
            
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result[0] if result and one else result

            conn.commit()
            return None
    except sqlite3.Error as e:
        print(f"[ERROR] DB Query failed: {e}")
        return [] if query.strip().lower().startswith("select") else None

