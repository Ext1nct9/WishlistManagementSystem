from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils

# Base URL for the API
BASE_URL = "http://localhost:8000/"

def setup_initial_accounts(db_path):
    try:
        # Initialize mock database
        clean_data(db_path)
        user_accounts = [
            (1, 'whamuzi@gmail.com', 'MrReborn', api_utils.hash_password('Abcdefghi1')),
            (2, 'mawpiew@gmail.com', 'Lost Boy', api_utils.hash_password('VixxenBibi#1')),
            (3, 'willy@gmail.com', 'tortue_perdue', api_utils.hash_password('jaimelest0rtues'))
        ]

        # Create a cursor for database operations
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


# Function to check if there is an account in the database
def account_exists(user_account_id, email, username, password):
    # Create a cursor for database operations
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if an account exists with the given user_id, email, username, and password
    cursor.execute('''SELECT * FROM UserAccount 
                      WHERE user_account_id = ? AND email = ? AND username = ?''', 
                   (user_account_id, email, username))

    # Fetch the first row (if any)
    user = cursor.fetchone()
    if user:
        if api_utils.verify_password(cursor, user[0], password):
            db_utils.close(conn, cursor)
            return True

    # Return True if a matching account was found, False otherwise
    db_utils.close(conn, cursor)
    return False


# Background

'''
@given('there exist the following user accounts')
def step_impl(context):
    # Call the setup function with the path
    setup_initial_accounts(DB_PATH)
'''

@given('the user {oldEmail}, {oldPassword} is logged into their account')
def is_logged_in(context, oldEmail, oldPassword):
    # Make a request to the login endpoint to authenticate the user
    context.response = requests.post(f'{BASE_URL}/login', json={"email": oldEmail, "password": oldPassword})
    context.auth_cookie = context.response.cookies.get('user_account_id')
    assert context.response.status_code == 200, "Login failed"


# Update an account successfully


@when('the user attempts to update their account {userAccountId} with valid inputs email {newEmail}, username {newUsername} and password {newPassword}')
def successful_update_account(context, userAccountId, newEmail, newUsername, newPassword):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.put(f'{BASE_URL}/update_account', json={"user_account_id": userAccountId, "email": newEmail, "username": newUsername, "password": newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for valid account update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200


@then('the old information with email {oldEmail}, username {oldUsername} and password {oldPassword} for account {userAccountId} shall no longer exist')
def before_update_account_shall_not_exist(context, userAccountId, oldEmail, oldUsername, oldPassword):
    assert not account_exists(userAccountId, oldEmail, oldUsername, oldPassword)


@then('the new information with email {newEmail}, username {newUsername} and password {newPassword} for account {userAccountId} shall exist')
def updated_account_shall_exist(context, userAccountId, newEmail, newUsername, newPassword):
    # Verify password
    

    # The expected account information
    expected_user_account = {
        "user_account_id": userAccountId,
        "email": newEmail,
        "username": newUsername,
    }

    assert account_exists(userAccountId, newEmail, newUsername, newPassword)
    assert context.response.json() == expected_user_account, "Response does not match the expected user account"


# Update an account unsuccessfully


@when('the user attempts to update their account {userAccountId} with invalid inputs email {newEmail}, username {newUsername} and password {newPassword}')
def unsuccessful_update_account(context, userAccountId, newEmail, newUsername, newPassword):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.put(f'{BASE_URL}/update_account', json={"user_account_id": userAccountId, "email": newEmail, "username": newUsername, "password": newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)


@when('the user attempts to update their account {userAccountId} with {newEmail} and username {newUsername}')
def unsuccessful_update_account(context, userAccountId, newEmail, newUsername):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.newPassword = ""
    context.response = requests.put(f'{BASE_URL}/update_account', json={"user_account_id": userAccountId, "email": newEmail, "username": newUsername, "password": context.newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)


@when('the user attempts to update their account {userAccountId} with email {newEmail} and password {newPassword}')
def unsuccessful_update_account(context, userAccountId, newEmail, newPassword):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.newUsername = ""
    context.response = requests.put(f'{BASE_URL}/update_account', json={"user_account_id": userAccountId, "email": newEmail, "username": context.newUsername, "password": newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)


@when('the user attempts to update their account {userAccountId} with username {newUsername} and password {newPassword}')
def unsuccessful_update_account(context, userAccountId, newUsername, newPassword):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.newEmail = ""
    context.response = requests.put(f'{BASE_URL}/update_account', json={"user_account_id": userAccountId, "email": context.newEmail, "username": newUsername, "password": newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)


@then('the new information with {newEmail}, username {newUsername} and password {newPassword} for account {userAccountId} shall not exist')
def updated_account_shall_not_exist(context, userAccountId, newEmail, newUsername, newPassword):
    assert not account_exists(userAccountId, newEmail, newUsername, newPassword)


@then('the old information with email {oldEmail}, username {oldUsername} and password {oldPassword} for account {userAccountId} shall still exist')
def before_update_account_shall_exist(context, userAccountId, oldEmail, oldUsername, oldPassword):
    assert account_exists(userAccountId, oldEmail, oldUsername, oldPassword)


@then('the system shall show the following error {error}')
def step_system_shows_error_message(context, error):
    response_data = context.response.json()
    print(response_data)
    assert response_data['error_msg'] == error
