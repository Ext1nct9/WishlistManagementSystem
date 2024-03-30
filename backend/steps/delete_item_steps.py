from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils
from initialize_DB import DB_PATH
from app import app

# Base URL for the API
BASE_URL = "http://localhost:8000/"

def setup_initial_accounts(db_path):
    try:
        clean_data(db_path)
        # Sample user account data
        user_account = [
            (1, 'tonyand@gmail.com', 'TonyAnde', api_utils.hash_password('Abcdefghi1')),
            (2, 'geminit@gmail.com', 'GeminiTa', api_utils.hash_password('Thaye12345'))
        ]

        conn, cursor = db_utils.conn()

        # Insert initial user accounts
        cursor.executemany('''INSERT INTO UserAccount (user_account_id, email, username, password)
                          VALUES (?, ?, ?, ?)''', user_account)

        # Commit changes and close the connection
        conn.commit()
        print("Initial accounts set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial accounts: {e}")

    db_utils.close(conn, cursor)


def setup_initial_wishlists(db_path):
    try:
        # Sample wishlist data
        wishlists = [
            (1, "School", "academic supplies", 1),
            (2, "Brunch", "breakfast lunch", 2)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial wishlists
        cursor.executemany('''INSERT INTO Wishlist (wishlist_id, name, description, user_account_id)
                          VALUES (?, ?, ?, ?)''', wishlists)

        # Commit changes and close the connection
        conn.commit()
        print("Initial wishlists set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial wishlists: {e}")

    db_utils.close(conn, cursor)

def setup_initial_items(db_path):
    try:
        # Sample wishlist data
        items = [
            (123, 'Pencil', 'for writing', 'staples.com', 1, 1, 1),
            (456, 'Eraser', 'for erasing', 'staples.ca', 1, 1, 1)
        ] 

        conn, cursor = db_utils.conn()

        # Insert initial wishlists
        cursor.executemany('''INSERT INTO Item (item_id, name, description, link, status, rank, wishlist_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', items)

        # Commit changes and close the connection
        conn.commit()
        print("Initial items set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial item: {e}")

    db_utils.close(conn, cursor)

def setup_initial_userPermission(db_path):
    try:
        # Sample wishlist data
        userPermissions = [
            (1, 1, 0b00000111),
            (2, 2, 0b00000000)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial wishlists
        cursor.executemany('''INSERT INTO UserPermission (user_account_id, wishlist_id, permissions)
                          VALUES (?, ?, ?)''', userPermissions)
    
        # Commit changes and close the connection
        conn.commit()
        print("Initial userPermission set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial userPermission: {e}")
    
    db_utils.close(conn, cursor)

def account_exists(user_account_id):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if an account exists with the given user_account_id
    cursor.execute('''SELECT * FROM UserAccount 
                      WHERE user_account_id = ?''', 
                   (user_account_id,))

    # Fetch the first row (if any)
    user = cursor.fetchone()
    if user:
        db_utils.close(conn, cursor)
        return True
    else:
        # Return True if a matching account was found, False otherwise
        # Close the connection
        db_utils.close(conn, cursor)
        return False

def userPermission_exists (user_account_id, wishlist_id, permissions):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a wishlist exists with the given user_account_id, and name
    cursor.execute('''SELECT permissions FROM UserPermission 
                      WHERE user_account_id = ? AND wishlist_id = ?''', 
                   (user_account_id, wishlist_id))

    # Fetch the first row (if any)
    permission_check = cursor.fetchone()
    if permission_check == permissions:
        db_utils.close(conn, cursor)
        return True

    else:
        # Return True if a matching account was found, False otherwise
        # Close the connection
        db_utils.close(conn, cursor)
        return False

# Function to check if there is a wishlist in the database
def item_exists (item_id, name, description):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a wishlist exists with the given user_account_id, and name
    cursor.execute('''SELECT * FROM Item 
                      WHERE item_id = ? AND name = ? AND description = ? ''', 
                   (item_id, name, description))

    # Fetch the first row (if any)
    item = cursor.fetchone()
    if item:
        db_utils.close(conn, cursor)
        return True

    else:
        # Return True if a matching account was found, False otherwise
        # Close the connection
        db_utils.close(conn, cursor)
        return False

# Function to get the wishlist id using the name
def get_wishlist_id (name):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a wishlist exists with the given user_account_id, and name
    cursor.execute('''SELECT wishlist_id FROM Wishlist 
                      WHERE name = ?''', 
                   (name))

    # Fetch the first row (if any)
    wishlist_id = cursor.fetchone()
    if wishlist_id:
        db_utils.close(conn, cursor)
        return True, wishlist_id

    else:
        # Return wishlist id if a matching wishlist was found, error otherwise
        # Close the connection
        db_utils.close(conn, cursor)
        return False, -1
 

@given ('the system has the following user account')
def step_impl(context):
    setup_initial_accounts(DB_PATH)

@given ('the system has the following wishlist')
def step_impl(context):
    setup_initial_wishlists(DB_PATH) 

@given ('the system has the following items')
def step_impl(context):
    setup_initial_items(DB_PATH)

@given ('the system has the following user permission')
def perm_impl(context):
    setup_initial_userPermission(DB_PATH)

@when('the valid user {validAccountId} requests to delete an item {validItemId}')
def delete_item_request(context, validAccountId, validItemId):
    context.user_account_id = validAccountId
    context.validItemId = validItemId

    #Request
    context.response = requests.delete(f'{BASE_URL}/delete_item/{validItemId}', 
                                       json={"user_account_id":validAccountId, "item_id":validItemId}, cookies={"user_account_id":context.user_account_id})

    # Log if not the right status code
    if context.response.status_code != 204:
        logging.info(context.response.text)
        logging.info((f"HTTP method used: {context.response.request.method}"))
        error_msg = f'Expected 204 status code for valid item deletion, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)
    assert context.response.status_code == 204

@when('the user {validAccountId} has permission {validPermission} to edit items {validWishlistId}')
def permission_exists(context, validAccountId, validPermission, validWishlistId):
    userPermission_exists(validAccountId, validWishlistId, validPermission)
    
@then('the item {validItemId} with the {oldName}, {oldDescription} shall no longer exist in the system')
def update_item_shall_not_exist(context, validItemId, oldName, oldDescription):
    assert not item_exists(validItemId, oldName, oldDescription)
