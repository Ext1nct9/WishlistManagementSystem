from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils, db_procedures
from initialize_DB import DB_PATH


# Base URL for the API
BASE_URL = "http://localhost:8000/"

def setup_initial_userPermission(db_path):
    try:
        # Sample wishlist data
        userPermissions = [
            (1, 4, 0b00000010),
            (2, 2, 0b00000010),
            (3, 3, 0b00000010),
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

def setup_initial_linkPermission(db_path):
    try:
        # Sample wishlist data
        linkPermissions = [
            (1, 2, 0b00000010),
            (2, 4, 0b00000010),
        ]

        conn, cursor = db_utils.conn()

        # Insert initial wishlists
        cursor.executemany('''INSERT INTO LinkPermission (link_permission_id, wishlist_id, permissions)
                          VALUES (?, ?, ?)''', linkPermissions)
    
        # Commit changes and close the connection
        conn.commit()
        print("Initial linkPermission set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial linkPermission: {e}")
    
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
 
@given ('there exists user permissions')
def setup_user_permission_to_edit(context):
    setup_initial_userPermission(DB_PATH)       

@given ('there exists link permissions')
def setup_link_permission_to_edit(context):
    setup_initial_linkPermission(DB_PATH)       

@when ('the valid user {ValidAccountId} request to update a wishlist {ValidWishlistId} with name {validName}, and description {validDescription}')
def check_user_wishlist(context, ValidAccountId, ValidWishlistId, validName, validDescription):

    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{ValidWishlistId}', json={"name" : validName, "description": validDescription}, cookies={"user_account_id":ValidAccountId})

    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200


@when ('the valid link {validLinkId} request to update a wishlist {ValidWishlistId} with name {validName}, and description {validDescription}')
def check_link_wishlist(context, validLinkId, ValidWishlistId, validName, validDescription):
    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{ValidWishlistId}?link_permission_id={validLinkId}', json={"name" : validName, "description": validDescription})

    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200


@then ('the {validWishlistId} with the {oldName} and {oldDescription} shall no longer exist')
def before_wishlist_shall_not_exist (context, validWishlistId, oldName, oldDescription):
    assert not wishlist_exists(validWishlistId, oldName, oldDescription)


@then ('the {validWishlistId} with the {validName} and {validDescription} shall exist')
def update_wishlist_shall_exist(context, validWishlistId, validName, validDescription):
    # The expected wishlist information
    expected_wishlist = {
        "wishlist_id": validWishlistId,
        "name": validName,
        "description": validDescription,
    }
    assert wishlist_exists(validWishlistId, validName, validDescription)
    print("Response JSON:", context.response.json())
    assert context.response.json() == expected_wishlist, "Response does not match the expected wishlist"


@when ('the invalid user {invalidAccountId} request to update a wishlist {ValidWishlistId} with name {validName}, and description {validDescription}')
def check_invalid_user_wishlist(context, invalidAccountId, ValidWishlistId, validName, validDescription):

    #Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{ValidWishlistId}', json={"name" : validName, "description": validDescription}, cookies={"user_account_id":invalidAccountId})

    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid user wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403
 

@then ('the {validWishlistId} with the {oldName} and {oldDescription} shall not exist')
def update_wishlist_shall_not_exist(context, validWishlistId, oldName, oldDescription):
    assert not wishlist_exists(validWishlistId, oldName, oldDescription)
                               

@when ('the invalid link {inValidLinkId} request to update a wishlist {validWishlistId} with name {validName}, and description {validDescription}')                             
def check_invalid_link_wishlist(context, inValidLinkId, validWishlistId, validName, validDescription):
    # Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{validWishlistId}?link_permission_id={inValidLinkId}', json={"name" : validName, "description": validDescription})
    
    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid link wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403


@when ('the user {validAccountId} request to update a wishlist {inValidWishlistId} with name {validName}, and description {validDescription}')
def check_invalid_wishlist(context, validAccountId, inValidWishlistId, validName, validDescription):
    # Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{inValidWishlistId}', json={"name" : validName, "description": validDescription}, cookies={"user_account_id":validAccountId})

    # Log if not the right status code
    if context.response.status_code != 404:
        error_msg = f'Expected 404 status code for invalid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 404


@when ('the user {validAccountId} request to update a wishlist {validWishlistId} with an empty name, and description {validDescription}')
def check_empty_name(context, validAccountId, validWishlistId, validDescription):
    context.name = ''
    # Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{validWishlistId}', json={"name" : context.name, "description": validDescription}, cookies={"user_account_id":validAccountId})

    # Log if not the right status code
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for empty name wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 400


@then ('the {validWishlistId} with an empty name and {validDescription} shall not exist')
def update_wishlist_empty_name_shall_not_exist(context, validWishlistId, validDescription):
    assert not wishlist_exists(validWishlistId, None, validDescription)

@when ('the user {validAccountId} request to update a wishlist {validWishlistId} with an existing name {inValidName}, and description {validDescription}')
def check_exist_name(context, validAccountId, validWishlistId, inValidName, validDescription):
    # Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{validWishlistId}', json={"name" : inValidName, "description": validDescription}, cookies={"user_account_id":validAccountId})

    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for existing name wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403


@then ('the {validWishlistId} with an existing name {inValidName} and {validDescription} shall not exist')
def update_wishlist_existing_name_shall_not_exist(context, validWishlistId, inValidName, validDescription):
    assert not wishlist_exists(validWishlistId, inValidName, validDescription)

@when ('the user {inValidAccountId}, with the link {inValidLinkId} requests to update a wishlist {validWishlistId} with name {validName}, and description {validDescription}')
def check_account_id_link_id(context, inValidAccountId, inValidLinkId, validWishlistId, validName, validDescription):
    # Request
    context.response = requests.put(f'{BASE_URL}/wishlist/update/{validWishlistId}?link_permission_id={inValidLinkId}', json={"name" : validName, "description": validDescription}, cookies={"user_account_id":inValidAccountId})

    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid user and link wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403
