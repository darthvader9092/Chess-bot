import sqlite3

def print_database(db_name):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM moves")
        rows = cursor.fetchall()
        
        if rows:
            print("ID | Move | Time Taken")
            for row in rows:
                print(f"{row[0]} | {row[1]} | {row[2]}")
        else:
            print("No data found in the database.")
            
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    finally:
        if connection:
            connection.close()

# Replace "X" with the name of your SQLite database
print_database("chess_game.db")
