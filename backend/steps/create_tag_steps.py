import sqlite3
import requests
from behave import given, when, then
from clean_DB import clean_data
from initialize_DB import DB_PATH
from utils import api_utils, db_utils

# Base URL for the API
BASE_URL = "http://localhost:8000/"

def setup_initial_accounts(db_path):
    try:
        clean_data(db_path)
        # Sample user account data
        user_accounts = [
            (1, 'whamuzi@gmail.com', 'MrReborn', api_utils.hash_password('Abcdefghi1')),
            (2, 'mawpiew@gmail.com', 'Lost Boy', api_utils.hash_password('VixxenBibi#1')),
            (3, 'willy@gmail.com', 'tortue_perdue', api_utils.hash_password('jaimelest0rtues'))
        ]

        conn, cursor = db_utils.conn()

        # Insert initial user accounts
        cursor.executemany('''INSERT INTO UserAccount (user_account_id, email, username, password)
                          VALUES (?, ?, ?, ?)''', user_accounts)

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
            (1,'Dress', 'dresses for me',1),
            (2,'Cars', 'dream cars',2),
            (3,'Books', 'favorite novels',3),
            (4,'Tech', 'gadgets and tech',3)  
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

def setup_initial_tags(db_path):
    try:
        # Sample tag data
        tags = [
            (1, 'Toys', 'Purple', 1),
            (2, 'Books', 'Blue', 2),
            (3, 'Music', 'Green', 3),
            (4, 'Food', 'Red', 4)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial tags
        cursor.executemany('''INSERT INTO Tag (tag_id, label, color, wishlist_id)
                          VALUES (?, ?, ?, ?)''', tags)
        
        # Commit changes and close the connection
        conn.commit()
        print("Initial tags set up successfully.")
    
    except sqlite3.Error as e:
        print(f"Error setting up initial tags: {e}")
    
    db_utils.close(conn, cursor)

def setup_initial_user_permissions(db_path):
    try:
        # Sample user permissions data
        user_permissions = [
            (1, 2, 0b00001001),
            (2, 1, 3),
            (3, 2, 0b00100011),
            (3, 1, 0b00001011)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial user permissions
        cursor.executemany('''INSERT INTO UserPermission (user_account_id, wishlist_id, permissions)
                          VALUES (?, ?, ?)''', user_permissions)
        
        # Commit changes and close the connection
        conn.commit()
        print("Initial user permissions set up successfully.")
    
    except sqlite3.Error as e:
        print(f"Error setting up initial user permissions: {e}")
    
    db_utils.close(conn, cursor)

def setup_initial_link_permissions(db_path):
    try:
        # Sample link permissions data
        link_permissions = [
            (1, 0b00001011, 1),
            (2, 0b00000101, 2),
            (3, 0b00001001, 3),
            (4, 0b00010001, 4)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial link permissions
        cursor.executemany('''INSERT INTO LinkPermission (link_permission_id, permissions, wishlist_id)
                          VALUES (?, ?, ?)''', link_permissions)
        
        # Commit changes and close the connection
        conn.commit()
        print("Initial link permissions set up successfully.")
    
    except sqlite3.Error as e:
        print(f"Error setting up initial link permissions: {e}")
    
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
def wishlist_exists (wishlist_id, name, description):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a wishlist exists with the given user_account_id, and name
    cursor.execute('''SELECT * FROM Wishlist 
                      WHERE wishlist_id = ? AND name = ? AND description = ? ''', 
                   (wishlist_id, name, description))

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
    
# Function to check if the tag exists in the database
def tag_exists (tag_id, label, color):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a tag exists with the given tag_id, label, and color
    cursor.execute('''SELECT * FROM Tag 
                      WHERE tag_id = ? AND label = ? AND color = ? ''', 
                   (tag_id, label, color))

    # Fetch the first row (if any)
    tag = cursor.fetchone()
    if tag:
        db_utils.close(conn, cursor)
        return True

    else:
        # Return True if a matching account was found, False otherwise
        # Close the connection
        db_utils.close(conn, cursor)
        return False

# Function to check if the user has permission to update wishlist
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


# Function to check if the user has permission to update wishlist
def linkPermission_exists (link_permission_id, wishlist_id, permissions):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a wishlist exists with the given user_account_id, and name
    cursor.execute('''SELECT permissions FROM LinkPermission 
                      WHERE link_permission_id = ? AND wishlist_id = ?''', 
                   (link_permission_id, wishlist_id))

    # Fetch the permission and check if edit permission matches
    permission_check = cursor.fetchone()
    if permission_check == permissions:
        db_utils.close(conn, cursor)
        return True

    else:
        # Return True if a matching account was found, False otherwise
        # Close the connection
        db_utils.close(conn, cursor)
        return False

#@given ('the following user accounts exist in the system')
#def step_impl(context):
#    setup_initial_accounts(DB_PATH)

@given ('the following wishlists exist in the system')
def step_impl(context):
    setup_initial_wishlists(DB_PATH)

@given ('the following tags exist in the system')
def step_impl(context):
    setup_initial_tags(DB_PATH)

@given ('the following user permissions exist in the system')
def step_impl(context):
    setup_initial_user_permissions(DB_PATH)

@given ('the following link permissions exist in the system')
def step_impl(context):
    setup_initial_link_permissions(DB_PATH)

@when('the valid user {ValidAccountId} in wishlist {WishlistID} enters a valid label {Label}, and a color {Color} for the tag')
def step_impl(context, ValidAccountId, WishlistID, Label, Color):
    context.wishlist_id = WishlistID
    
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/{WishlistID}/create_tag', json={"label": Label, "color": Color}, cookies ={"user_account_id": ValidAccountId})

    # Log if not the right status code
    if context.response.status_code != 201:
        error_msg = f'Expected 201 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 201

@then('a tag with an automatically assigned ID, label {Label}, and color {Color} shall be created under the wishlist {WishlistID}')
def step_impl(context, Label, Color, WishlistID):
    # Check if the tag exists
    expected_tag = {
        "tag_id": context.response.json()["tag_id"],
        "label": Label,
        "color": Color,
        "wishlist_id": WishlistID,
    }
    assert "tag_id" in context.response.json(), "Tag ID not found in response"
    assert "label" in context.response.json(), "Label not found in response"
    assert "color" in context.response.json(), "Color not found in response"    
    assert "wishlist_id" in context.response.json(), "Wishlist ID not found in response"
    assert context.response.json() == expected_tag, f"Expected {expected_tag}, but got {context.response.json()}"

@when('the valid user {ValidAccountId} in wishlist {WishlistID} enters a valid label {Label}, and does not provide a color for the tag')
def step_impl(context, ValidAccountId, WishlistID, Label):
    context.wishlist_id = WishlistID
    
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/{WishlistID}/create_tag', json={"label": Label}, cookies ={"user_account_id": ValidAccountId})

    # Log if not the right status code
    if context.response.status_code != 201:
        error_msg = f'Expected 201 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 201

@then('a tag with an automatically assigned ID, label {Label}, and a random color shall be created under the wishlist {WishlistID}')
def step_impl(context, Label, WishlistID):
    # Check if the tag exists
    expected_tag = {
        "tag_id": context.response.json()["tag_id"],
        "label": Label,
        "color": context.response.json()["color"],
        "wishlist_id": WishlistID,
    }
    assert "tag_id" in context.response.json(), "Tag ID not found in response"
    assert "label" in context.response.json(), "Label not found in response"
    assert "color" in context.response.json(), "Color not found in response"    
    assert "wishlist_id" in context.response.json(), "Wishlist ID not found in response"
    assert context.response.json() == expected_tag, f"Expected {expected_tag}, but got {context.response.json()}"

@when('the valid user {ValidAccountId} in wishlist {WishlistID} does not provide a label for the tag')
def step_impl(context, ValidAccountId, WishlistID):
    context.wishlist_id = WishlistID
    
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/{WishlistID}/create_tag', json ={}, cookies ={"user_account_id": ValidAccountId})

    # Log if not the right status code
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for invalid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 400

@then('a tag shall not be created under the wishlist {WishlistID}')
def step_impl(context, WishlistID):
    # Check if the tag exists
    assert not "tag_id" in context.response.json(), "Tag ID found in response"
    assert not "label" in context.response.json(), "Label found in response"
    assert not "color" in context.response.json(), "Color found in response"    
    assert not "wishlist_id" in context.response.json(), "Wishlist ID found in response"
    assert "error_msg" in context.response.json()

@when('the valid user {ValidAccountId} in wishlist {WishlistID} enters a label {Label} for the tag that already exists in the wishlist')
def step_impl(context, ValidAccountId, WishlistID, Label):
    context.wishlist_id = WishlistID
    
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/{WishlistID}/create_tag', json={"label": Label}, cookies ={"user_account_id": ValidAccountId})

    # Log if not the right status code
    if context.response.status_code != 409:
        error_msg = f'Expected 409 status code for invalid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 409

@when('the invalid user {InvalidAccountId} in wishlist {WishlistID} enters a valid label {Label}, and a color {Color} for the tag')
def step_impl(context, InvalidAccountId, WishlistID, Label, Color):
    context.wishlist_id = WishlistID
    
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/{WishlistID}/create_tag', json={"label": Label, "color": Color}, cookies ={"user_account_id": InvalidAccountId})

    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403

@when ('the user with valid permission link {ValidPermissionLink} in wishlist {WishlistID} enters a valid label {Label}, and a color {Color} for the tag')
def step_impl(context, ValidPermissionLink, WishlistID, Label, Color):
    context.wishlist_id = WishlistID
    
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/{WishlistID}/create_tag', json={"label": Label, "color": Color}, params={"link_permission_id": ValidPermissionLink})

    # Log if not the right status code
    if context.response.status_code != 201:
        error_msg = f'Expected 201 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 201

@when ('the user with invalid permission link {InvalidPermissionLink} in wishlist {WishlistID} enters a valid label {Label}, and a color {Color} for the tag')
def step_impl(context, InvalidPermissionLink, WishlistID, Label, Color):
    context.wishlist_id = WishlistID
    
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/{WishlistID}/create_tag', json={"label": Label, "color": Color}, params={"link_permission_id": InvalidPermissionLink})

    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid wishlist update, but got {context.response.status_code}.'
        # raise AssertionError(error_msg)
        raise AssertionError(context.response.json()["WTF"])
    assert context.response.status_code == 403
