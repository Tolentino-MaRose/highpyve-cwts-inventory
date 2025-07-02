import sqlite3

DB = 'database.db'

def display_table(table_name):
    """Display all rows from the specified table."""
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        print(f"\n=== {table_name.upper()} TABLE ===")
        if not rows:
            print("No records found.\n")
            return

        headers = rows[0].keys()
        print(" | ".join(headers))
        print("-" * (len(headers) * 15))

        for row in rows:
            print(" | ".join(str(row[h]) for h in headers))


def main():
    """Main viewer function for the CWTS Inventory database."""
    print("CWTS Inventory System")
    display_table('Item')
    display_table('Log')


if __name__ == '__main__':
    main()
