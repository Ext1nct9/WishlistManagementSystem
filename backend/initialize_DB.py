import sqlite3 as sql
from sqlite3 import Cursor
from clean_DB import clean_database
import os

# DB file path
current_directory = os.path.dirname(__file__)
DB_PATH = os.path.join(current_directory, "database.db")
print("Database File Path: ", DB_PATH)


# Initialize the whole database (every table)
def initialize_entire_DB():
    print('DB initialization started...')

    conn = sql.connect(DB_PATH)
    print('DB connection established')

    c = conn.cursor()

    print('Enabling foreign keys with Pragma. Read about Pragma at https://www.sqlite.org/pragma.html')
    c.execute('PRAGMA foreign_keys = ON')

    print('Creating tables...')

    print('Creating UserAccount table...')
    initialize_DBtable_UserAccount(c)

    # [TODO] Maybe: initialize_DBtable_Friends(c)

    print('Creating Wishlist table...')
    initialize_DBtable_Wishlist(c)

    print('Creating UserPermission table...')
    initialize_DBtable_UserPermission(c)

    print('Creating LinkPermission table...')
    initialize_DBtable_LinkPermission(c)

    print('Creating Item table...')
    initialize_DBtable_Item(c)

    print('Creating Tag table...')
    initialize_DBtable_Tag(c)

    print('Creating ItemTag table...')
    initialize_DBtable_ItemTag(c)

    print('Creating Comment table...')
    initialize_DBtable_Comment(c)

    print('Tables created')

    conn.commit()
    print('DB commit successful')

    conn.close()

    print('DB initialization finished')


# UserAccount table
def initialize_DBtable_UserAccount(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS UserAccount (
            user_account_id TEXT PRIMARY KEY UNIQUE NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            pfp BLOB
        )
    ''')
    # [TODO] Maybe: isPublic BOOLEAN NOT NULL
    # [TODO] Maybe: wishlist_order TEXT


# Friends table
def initialize_DBtable_Friends(c: Cursor):
    # [TODO] Maybe: Friends table
    pass


# Wishlist table
def initialize_DBtable_Wishlist(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS Wishlist (
            wishlist_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            user_account_id TEXT NOT NULL,
            FOREIGN KEY (user_account_id) REFERENCES UserAccount(user_account_id) ON DELETE CASCADE,
            PRIMARY KEY (wishlist_id)
        )
    ''')
    # [TODO] Maybe: access_permissions TINYINT NOT NULL
    # [TODO] Maybe: cover_photo BLOB
    # [TODO] Maybe: rank INTEGER OR TEXT


# UserPermission table
def initialize_DBtable_UserPermission(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS UserPermission (
            user_account_id TEXT NOT NULL,
            wishlist_id TEXT NOT NULL,
            permissions TINYINT NOT NULL,
            FOREIGN KEY (wishlist_id) REFERENCES Wishlist(wishlist_id) ON DELETE CASCADE,
            FOREIGN KEY (user_account_id) REFERENCES UserAccount(user_account_id) ON DELETE CASCADE,
            PRIMARY KEY (user_account_id, wishlist_id)
        )
    ''')


# LinkPermission table
def initialize_DBtable_LinkPermission(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS LinkPermission (
            link_permission_id TEXT UNIQUE NOT NULL,
            permissions TINYINT NOT NULL,
            wishlist_id TEXT NOT NULL,
            FOREIGN KEY (wishlist_id) REFERENCES Wishlist(wishlist_id) ON DELETE CASCADE,
            PRIMARY KEY (link_permission_id)
        )
    ''')


# Item table
def initialize_DBtable_Item(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            item_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            image BLOB,
            link TEXT,
            status TINYINT NOT NULL,
            rank INTEGER UNSIGNED,
            wishlist_id TEXT NOT NULL,
            FOREIGN KEY (wishlist_id) REFERENCES Wishlist(wishlist_id) ON DELETE CASCADE,
            PRIMARY KEY (item_id)
        )
    ''')


# Tag table
def initialize_DBtable_Tag(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS Tag (
            tag_id TEXT UNIQUE NOT NULL,
            label TEXT NOT NULL,
            color TEXT NOT NULL,
            wishlist_id TEXT NOT NULL,
            FOREIGN KEY (wishlist_id) REFERENCES Wishlist(wishlist_id) ON DELETE CASCADE,
            PRIMARY KEY (tag_id)
        )   
    ''')


# ItemTag table
def initialize_DBtable_ItemTag(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS ItemTag (
            item_id TEXT NOT NULL,
            tag_id TEXT NOT NULL,
            FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES Tag(tag_id) ON DELETE CASCADE,
            PRIMARY KEY (item_id, tag_id)
        )
    ''')


# Comment table
def initialize_DBtable_Comment(c: Cursor):
    c.execute('''
        CREATE TABLE IF NOT EXISTS Comment (
            comment_id TEXT UNIQUE NOT NULL,
            user_info TEXT NOT NULL,
            is_account BOOLEAN NOT NULL,
            body TEXT NOT NULL,
            item_id TEXT NOT NULL,
            creation_datetime INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
            FOREIGN KEY (item_id) REFERENCES Item(item_id) ON DELETE CASCADE,
            PRIMARY KEY (comment_id)
        )
    ''')


if __name__ == '__main__':
    clean_database(DB_PATH)
    initialize_entire_DB()

