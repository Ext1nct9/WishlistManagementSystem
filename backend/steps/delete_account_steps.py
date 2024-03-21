from behave import given, when, then
from flask import request, make_response
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
def account_exists(user_account_id):
    # Create a cursor for database operations
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if an account exists with the given user_id, email, username, and password
    cursor.execute('''SELECT * FROM UserAccount 
                      WHERE user_account_id = ?''', 
                   (user_account_id))

    # Fetch the first row (if any)
    user = cursor.fetchone()
    if user:
        db_utils.close(conn, cursor)
        return True

    # Return True if a matching account was found, False otherwise
    db_utils.close(conn, cursor)
    return False


# Function to check how many accounts there are in the system
def account_count():
    # Create a cursor for database operations
    conn, cursor = db_utils.conn()

    cursor.execute('''SELECT COUNT(user_account_id) 
                    FROM UserAccount
                    ''')

    count = cursor.fetchone()[0]
    db_utils.close(conn, cursor)

    return count
    

# Background

'''
@given('there exist the following user accounts')
def step_impl(context):
    # Call the setup function with the path
    setup_initial_accounts(DB_PATH)
'''
"""
@given('the user {email}, {password} is logged into their account')
def is_logged_in(context, oldEmail, oldPassword):
    # Make a request to the login endpoint to authenticate the user
    context.response = requests.post(f'{BASE_URL}/login', json={"email": oldEmail, "password": oldPassword})
    context.auth_cookie = context.response.cookies.get('user_account_id')
    assert context.response.status_code == 200, "Login failed"
"""


# Delete an account successfully


@when('the user attempts to delete their account {userAccountId}')
def successful_delete_account(context, userAccountId):
    # Get the account count before deleting
    context.count = account_count()

    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.delete(f'{BASE_URL}/delete_account', json={"user_account_id": userAccountId}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code != 204:
        logging.info(context.response)
        error_msg = f'Expected 204 status code for valid account deletion, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 204


@then('the user {userAccountId} shall no longer exist')
def account_shall_no_longer_exist(context, userAccountId):
    assert not account_exists(userAccountId)


@then('the total number of accounts shall be {numAccounts}')
def accounts_final_count(context, numAccounts):
    assert ((context.count - 1), numAccounts)
