# import sqlite3

# def add_vacation_table():
#     conn = sqlite3.connect("schedule.db")
#     cursor = conn.cursor()

#     # Create Vacation table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Vacation (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         toggle_mode INTEGER DEFAULT 0, -- 0 for off, 1 for on
#         start_date TEXT,              -- Start date in YYYY-MM-DD
#         end_date TEXT                 -- End date in YYYY-MM-DD
#     )
#     """)

#     # Initialize a row if it doesn't exist
#     cursor.execute("SELECT COUNT(*) FROM Vacation")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO Vacation (toggle_mode) VALUES (0)")

#     conn.commit()
#     conn.close()

# add_vacation_table()


import sqlite3

def rebuild_vacation_table():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    # Drop the existing Vacation table if it exists
    cursor.execute("DROP TABLE IF EXISTS Vacation")

    # Recreate the Vacation table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Vacation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        toggle_mode INTEGER DEFAULT 0, -- 0 for off, 1 for on
        start_date TEXT,              -- Start date in YYYY-MM-DD
        end_date TEXT                 -- End date in YYYY-MM-DD
    )
    """)

    # Insert a row to initialize it
    cursor.execute("INSERT INTO Vacation (toggle_mode) VALUES (0)")
    conn.commit()
    conn.close()

    print("Vacation table has been rebuilt and initialized.")

if __name__ == "__main__":
    rebuild_vacation_table()

