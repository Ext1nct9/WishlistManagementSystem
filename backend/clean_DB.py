import sqlite3

 # Clean data from database
def clean_data(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Delete all data from the tables
        cursor.execute("DELETE FROM UserAccount")
        cursor.execute("DELETE FROM UserPermission")
        cursor.execute("DELETE FROM Wishlist")
        cursor.execute("DELETE FROM LinkPermission")
        cursor.execute("DELETE FROM Tag")
        cursor.execute("DELETE FROM ItemTag")
        cursor.execute("DELETE FROM Item")
        cursor.execute("DELETE FROM Comment")


        # Commit the transaction to apply changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error cleaning database: {e}")

    finally:
        if conn:
            conn.close()

 # Clean database and all the tables
def clean_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Delete all data from the tables
        cursor.execute("DROP TABLE IF EXISTS UserAccount")
        cursor.execute("DROP TABLE IF EXISTS UserPermission")
        cursor.execute("DROP TABLE IF EXISTS Wishlist")
        cursor.execute("DROP TABLE IF EXISTS LinkPermission")
        cursor.execute("DROP TABLE IF EXISTS Tag")
        cursor.execute("DROP TABLE IF EXISTS ItemTag")
        cursor.execute("DROP TABLE IF EXISTS Item")
        cursor.execute("DROP TABLE IF EXISTS Comment")
        # Add more DELETE statements if you have other tables
        cursor.execute("DROP TABLE IF EXISTS Wishlist")
        cursor.execute("DROP TABLE IF EXISTS UserPermission")
        cursor.execute("DROP TABLE IF EXISTS LinkPermission")
        # Commit the transaction to apply changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error cleaning database: {e}")

    finally:
        if conn:
            conn.close()