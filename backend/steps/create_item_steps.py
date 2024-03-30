from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils
from initialize_DB import DB_PATH

# Base URL for the API
BASE_URL = "http://localhost:8000/"

def setup_initial_accounts(db_path):
    try:
        clean_data(db_path)
        # Sample user account data
        user_account = [
            (1, 'hera@gmail.com', 'Hera', api_utils.hash_password('Abcdefghi1')),
            (2, 'zeus@gmail.com', 'Zeus', api_utils.hash_password('Thaye12345'))
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


def setup_initial_wishlists():
    try:
        # Sample wishlist data
        wishlists = [
            (324, "School", "academic supplies", 1),
            (735, "Brunch", "breakfast lunch", 2)
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

def setup_initial_items():
    try:
        # Sample wishlist data
        items = [
            (908, "Pencil", "for writing", "staples.com", 1, 1, 1)
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

# Function to check if there is a wishlist in the database
def wishlist_exists (user_account_id, description, name):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a wishlist exists with the given user_account_id, and name
    cursor.execute('''SELECT * FROM Wishlist 
                      WHERE user_account_id = ? AND name = ?''', 
                   (user_account_id, name))

    # Fetch the first row (if any)
    wishlist = cursor.fetchone()
    if wishlist:
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
 

@given ('the system contains the following initial user accounts')
def step_impl(context):
    setup_initial_accounts(DB_PATH)

@given ('the system contains the following initial wishlists')
def step_impl(context):
    setup_initial_wishlists() 

@given ('the following item exists in the system')
def step_impl(context):
    setup_initial_items()

@given ('the user {userID} owns wishlist {wishlistID} with name {wishlistName}')
def user_owns_wishlist(context, userID, wishlistID, wishlistName):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Query UserPermission
    cursor.execute('''
        SELECT * FROM wishlist
        WHERE user_account_id = ? AND wishlist_id = ? AND name = ?;
    ''', (userID, wishlistID, wishlistName))
    result = cursor.fetchone()

    # Check if Wishlist exists
    assert result is not None

    # Commit and close connection
    db_utils.close(conn, cursor, False)

@given ('the user is logged in with email {email} and password {password}')
def logged(context, email, password):

    print(f"Logging in as user with email {email}...")

    response = requests.post(api_utils.BASE_URL + "/login", json={"email": email, "password": password})

    assert response.status_code == 200, f"Error: {response.json()}"

    print(f"Successfully logged in.")

    context.cookies = response.cookies.get_dict()  # persist cookies for the next steps

@when ('the user enters a valid wishlist ID {validWishlistID}, a valid item name {validName}, and a description {description}')
def valid_user_and_item(context, validWishlistID, validName, description):
    context.wishlist = validWishlistID
    context.name = validName
    context.description = description
    context.response = requests.post(f'{BASE_URL}/create_item/{validWishlistID}', json={"name": validName, "description": description, "wishlist_id": validWishlistID, "status": "created"}, cookies=context.cookies)    #Log if not the right status code
    if context.response.status_code != 201:
        logging.info(context.response.text)
        logging.info(context.wishlist)
        error_msg = f'Expected 201 status code for valid creation, but got {context.response.status_code}.'
        logging.error(error_msg)
        error_msg = f'Got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)
    assert context.response.status_code == 201

@then('the item {item} with description {description} shall exist under {validWishlistID}')
def wishlist_shall_exist(context, item, description, validWishlistID):
    #Check if wishlist exists
    expected_wishlist = {
        "item_id": context.response.json()["item_id"],
        "name": item,
        "description": description,
        "wishlist_id": validWishlistID,
    }

    assert "item_id" in context.response.json(), "Failed to retrieve item ID"
    assert context.response.json()["item_id"] == expected_wishlist["item_id"], "Response does not match the expected item"
    assert "name" in context.response.json(), "Failed to retrieve item name"
    assert context.response.json()["name"] == expected_wishlist["name"], "Response does not match the expected item"
    assert "description" in context.response.json(), "Failed to retrieve description"
    assert context.response.json()["description"] == expected_wishlist["description"], "Response does not match the expected item"
    assert "wishlist_id" in context.response.json(), "Failed to retrieve wishlist"
    assert context.response.json()["wishlist_id"] == expected_wishlist["wishlist_id"], "Response does not match the expected item"