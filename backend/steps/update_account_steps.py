from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils
from app import app

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


# Update an account successfully

@given('the user with email {oldEmail}, {password} is logged into their account')
def is_logged_in(context, oldEmail, password):
    # Make a request to the login endpoint to authenticate the user
    context.response = requests.post(f'{BASE_URL}/login', json={"email": oldEmail, "password": password})
    context.auth_cookie = context.response.cookies.get('user_account_id')
    assert context.response.status_code == 200, "Login failed"

@given('the user with {email}, {password} is logged into their account')
def is_logged_in(context, email, password):
    # Make a request to the login endpoint to authenticate the user
    context.response = requests.post(f'{BASE_URL}/login', json={"email": email, "password": password})
    context.auth_cookie = context.response.cookies.get('user_account_id')
    assert context.response.status_code == 200, "Login failed"

@given('the user {email}, {oldPassword} is logged into their account')
def is_logged_in(context, email, oldPassword):
    # Make a request to the login endpoint to authenticate the user
    context.response = requests.post(f'{BASE_URL}/login', json={"email": email, "password": oldPassword})
    context.auth_cookie = context.response.cookies.get('user_account_id')
    assert context.response.status_code == 200, "Login failed"


@when('the user attempts to update their account {userAccountId} with valid input email {newEmail}')
def successful_update_account_email(context, userAccountId, newEmail):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.put(f'{BASE_URL}/update_account_email', json={"user_account_id": userAccountId, "email": newEmail}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for valid account update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200

@when('the user attempts to update their account {userAccountId} with valid input username {newUsername}')
def successful_update_account_username(context, userAccountId, newUsername):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.put(f'{BASE_URL}/update_account_username', json={"user_account_id": userAccountId, "username": newUsername}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for valid account update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200

@when('the user attempts to update their account {userAccountId} with valid input password {newPassword}')
def successful_update_account_password(context, userAccountId, newPassword):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.put(f'{BASE_URL}/update_account_password', json={"user_account_id": userAccountId, "password": newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for valid account update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200


@then('the old account with information with email {oldEmail}, username {username} and password {password} for account {userAccountId} shall no longer exist')
def before_update_email_account_shall_not_exist(context, userAccountId, oldEmail, username, password):
    assert not account_exists(userAccountId, oldEmail, username, password)

@then('the old account information with email {email}, username {oldUsername} and password {password} for account {userAccountId} shall no longer exist')
def before_update_username_account_shall_not_exist(context, userAccountId, email, oldUsername, password):
    assert not account_exists(userAccountId, email, oldUsername, password)

@then('the old information with email {email}, username {username} and password {oldPassword} for account {userAccountId} shall no longer exist')
def before_update_password_account_shall_not_exist(context, userAccountId, email, username, oldPassword):
    assert not account_exists(userAccountId, email, username, oldPassword)


@then('the new account with information with email {newEmail}, username {username} and password {password} for account {userAccountId} shall exist')
def updated_email_account_shall_exist(context, userAccountId, newEmail, username, password):    
    # The expected account information
    expected_user_account = {
        "user_account_id": userAccountId,
        "email": newEmail,
        "username": username,
    }

    assert account_exists(userAccountId, newEmail, username, password)
    assert context.response.json() == expected_user_account, "Response does not match the expected user account"

@then('the new account information with email {email}, username {newUsername} and password {password} for account {userAccountId} shall exist')
def updated_username_account_shall_exist(context, userAccountId, email, newUsername, password):    
    # The expected account information
    expected_user_account = {
        "user_account_id": userAccountId,
        "email": email,
        "username": newUsername,
    }

    assert account_exists(userAccountId, email, newUsername, password)
    assert context.response.json() == expected_user_account, "Response does not match the expected user account"

@then('the new information with email {email}, username {username} and password {newPassword} for account {userAccountId} shall exist')
def updated_password_account_shall_exist(context, userAccountId, email, username, newPassword):    
    # The expected account information
    expected_user_account = {
        "user_account_id": userAccountId,
        "email": email,
        "username": username,
    }

    assert account_exists(userAccountId, email, username, newPassword)
    assert context.response.json() == expected_user_account, "Response does not match the expected user account"


# Update an account unsuccessfully
        

@when('the user attempts to update their account {userAccountId} with an empty email')
def unsuccessful_email_update_account(context, userAccountId):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.newEmail = ""
    context.response = requests.put(f'{BASE_URL}/update_account_email', json={"user_account_id": userAccountId, "email": context.newEmail}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)

@when('the user attempts to update their account {userAccountId} with an empty username')
def unsuccessful_username_update_account(context, userAccountId):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.newUsername = ""
    context.response = requests.put(f'{BASE_URL}/update_account_username', json={"user_account_id": userAccountId, "username": context.newUsername}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)

@when('the user attempts to update their account {userAccountId} with an empty password')
def unsuccessful_password_update_account(context, userAccountId):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.newPassword = ""
    context.response = requests.put(f'{BASE_URL}/update_account_password', json={"user_account_id": userAccountId, "password": context.newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)

@when('the user attempts to update their account {userAccountId} with invalid input password {newPassword}')
def unsuccessful_update_password_account(context, userAccountId, newPassword):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.put(f'{BASE_URL}/update_account_password', json={"user_account_id": userAccountId, "password": newPassword}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid account update.'
        raise AssertionError(error_msg)


@then('the new account with information with {newEmail}, username {username} and password {password} for account {userAccountId} shall not exist')
def updated_email_account_shall_not_exist(context, userAccountId, newEmail, username, password):
    assert not account_exists(userAccountId, newEmail, username, password)

@then('the new account information with {email}, username {newUsername} and password {password} for account {userAccountId} shall not exist')
def updated_username_account_shall_not_exist(context, userAccountId, email, newUsername, password):
    assert not account_exists(userAccountId, email, newUsername, password)

@then('the new information with {email}, username {username} and password {newPassword} for account {userAccountId} shall not exist')
def updated_password_account_shall_not_exist(context, userAccountId, email, username, newPassword):
    assert not account_exists(userAccountId, email, username, newPassword)


@then('the old account with information with email {oldEmail}, username {username} and password {password} for account {userAccountId} shall still exist')
def before_email_update_account_shall_exist(context, userAccountId, oldEmail, username, password):
    assert account_exists(userAccountId, oldEmail, username, password)

@then('the old account information with email {email}, username {oldUsername} and password {password} for account {userAccountId} shall still exist')
def before_username_update_account_shall_exist(context, userAccountId, email, oldUsername, password):
    assert account_exists(userAccountId, email, oldUsername, password)

@then('the old information with email {email}, username {username} and password {oldPassword} for account {userAccountId} shall still exist')
def before_password_update_account_shall_exist(context, userAccountId, email, username, oldPassword):
    assert account_exists(userAccountId, email, username, oldPassword)


@then('the system shall show the following error {error}')
def step_system_shows_error_message(context, error):
    response_data = context.response.json()
    print(response_data)
    assert response_data['error_msg'] == error
