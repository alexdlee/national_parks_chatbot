import sqlite3

def create_table():
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT,
        highlights TEXT,
        best_time TEXT
    )             
    """)

    cursor.execute("""
INSERT INTO parks (name, location, description, highlights, best_time)
VALUES (?, ?, ?, ?, ?)
""", ("Yellowstone", "Wyoming, Montana, Idaho", 
      "Famous for geysers and hot springs.", 
      "Old Faithful, Grand Prismatic Spring", 
      "April to October"))

    cursor.execute("""
INSERT INTO parks (name, location, description, highlights, best_time)
VALUES (?, ?, ?, ?, ?)
""", ("Yosemite", "California", 
      "Known for its giant sequoia trees and iconic cliffs.", 
      "El Capitan, Half Dome, Yosemite Falls", 
      "May to September"))
    


    conn.commit()
    conn.close()

create_table()


def check_database():
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()

    # Fetch and print all rows from the parks table
    cursor.execute("SELECT * FROM parks")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

check_database()

