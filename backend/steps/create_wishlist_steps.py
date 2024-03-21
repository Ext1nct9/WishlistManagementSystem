from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils, db_procedures
from initialize_DB import DB_PATH


# Base URL for the API
BASE_URL = "http://localhost:8000/"

def setup_initial_accounts(db_path):
    try:
        clean_data(db_path)
        # Sample user account data
        user_accounts = [
            (1, 'whamuzi@gmail.com', 'MrReborn', api_utils.hash_password('Abcdefghi!')),
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
            (1, "Dress", "dresses for me" ,1),
            (2, "Cars", "dream cars", 1),
            (3, "Books", "favorite novels", 1),
            (4, "Tech", "gadgets and tech", 2)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial wishlists
        cursor.executemany('''INSERT INTO Wishlist (wishlist_id, name, description, user_account_id)
                          VALUES (?, ?, ?, ?)''', wishlists)
    
        # Commit changes and close the connection
        conn.commit()
        print("Initial wishlists set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial accounts: {e}")
    
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
 

@given ('the following user accounts exist in the system')
def setup_user_accounts(context):
    setup_initial_accounts(DB_PATH)   

@given ('there exists following wishlists')
def setup_wishlists(context):
    setup_initial_wishlists(DB_PATH) 

@when ('the valid user {ValidAccountId} enters a valid wishlist name {validName}, and a description {Description}')
def valid_user_and_name(context, ValidAccountId, validName, Description):
    #Request
    context.user_account_id = ValidAccountId
    context.name = validName
    context.description = Description
    context.response = requests.post(f'{BASE_URL}/wishlist/create/{context.user_account_id}', json={"name": context.name, "description": context.description}, cookies={"user_account_id":context.user_account_id})
    #Log if not the right status code
    if context.response.status_code != 201:
        error_msg = f'Expected 201 status code for valid creation, but got {context.response.status_code}.'
        logging.error(error_msg)
        error_msg = f'Got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)
    assert context.response.status_code == 201

@then ('the wishlist {validName} with dsecription {Description} shall exist under {ValidAccountId}')
def wishlist_shall_exist(context, ValidAccountId, validName, Description):
    #Check if wishlist exists
    expected_wishlist = {
        "wishlist_id": context.response.json()["wishlist_id"],
        "name": validName,
        "description": Description,
        "user_account_id" : ValidAccountId,
    }
    assert "wishlist_id" in context.response.json(), "Failed to retrieve wishlist ID"
    assert "name" in context.response.json(), "Failed to retrieve user account email"
    assert "description" in context.response.json(), "Failed to retrieve username"
    assert "user_account_id" in context.response.json(), "Failed to retrieve username"
    assert context.response.json() == expected_wishlist, "Response does not match the expected user account"


@when ('the user {ValidAccountId} enters an invalid wishlist name {invalidName}, and a description {Description}')
def invalid_name (context, ValidAccountId, invalidName, Description):
    
    context.user_account_id = ValidAccountId
    context.name = invalidName
    context.description = Description

    log_existing_wishlists(context.user_account_id)

    context.response = requests.post(f'{BASE_URL}/wishlist/create/{context.user_account_id}', json={"name": context.name, "description": context.description}, cookies={"user_account_id":context.user_account_id})
    #Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid wishlist name, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)

@then ('the wishlist {invalidName} with description {Description} shall not exist under {ValidAccountId} because of an invalid name')
def name_already_exist(context, invalidName, Description, ValidAccountId):
    #check if wishlist exists
    wishlist_exists_result = wishlist_exists(ValidAccountId, Description, invalidName)
    #On false, print the message
    assert wishlist_exists_result, f"Wishlist with name '{invalidName}', and user account id '{ValidAccountId}' already exists."

@then('an wishlist shall not be created due to the exsiting name')
def wishlist_not_created_name(context):
    assert context.response.status_code == 403


@when ('the user {ValidAccountId} enters an empty wishlist name, and a description {Description}')
def missing_name (context, ValidAccountId, Description):
    context.user_account_id = ValidAccountId
    context.name = ''
    context.description = Description
    
    # Send POST request to create a wishlist without name
    context.response = requests.post(f'{BASE_URL}/wishlist/create/{context.user_account_id}', json={"name": context.name, "description": context.description}, cookies={"user_account_id":context.user_account_id})


@then ('the wishlist with description {Description} shall not exist under {ValidAccountId} because of an empty wishlist name')
def missing_name_error(context, Description, ValidAccountId):
    #Log if not the right status
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for missing name, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)
  
 
@then ('the system shall display the following error message {message}')
def step_system_displays_error_message(context, message):
    response_data = context.response.json()
    
    assert response_data['error_msg'] == message


@then ('an wishlist shall not be created due to the empty name')
def no_wishlist_created(context):
    assert context.response.status_code == 400


@when ('the user {inValidAccountId} enters a valid wishlist name {validName}, and a description {Description}')
def invalid_user (context, inValidAccountId, validName, Description):
    context.user_account_id = inValidAccountId
    context.name = validName
    context.description = Description
    context.response = requests.post(f'{BASE_URL}/wishlist/create/{context.user_account_id}', json={"name": context.name, "description": context.description},cookies={"user_account_id":context.user_account_id})
    #Log if not the right status code
    if context.response.status_code != 404:
        error_msg = f'Expected 404 status code for invalid user account id, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg) 


@then ('the wishlist {validName} with description {Description} shall not exist becuase of {inValidAccountId} user')
def invalid_user_error(context, validName, Description, inValidAccountId):
    no_account = account_exists (inValidAccountId)
    assert not no_account,  f"Wishlist with name '{validName}', description '{Description}', and user account id '{inValidAccountId}' exists, but it shouldn't."

    
@then ('a wishlist shall not be created due to invalid user id')
def no_wishlist_created(context):
    assert context.response.status_code == 404
    

def log_existing_wishlists(user_account_id):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to retrieve existing wishlists for the specified user_account_id
    cursor.execute('''
        SELECT * FROM Wishlist 
        WHERE user_account_id = ?
        ''', (user_account_id,))

    existing_wishlists = cursor.fetchall()

    # Log existing wishlists
    logging.info(f'Existing wishlists for user_account_id {user_account_id}: {existing_wishlists}')

    # Close the connection
    db_utils.close(conn, cursor)