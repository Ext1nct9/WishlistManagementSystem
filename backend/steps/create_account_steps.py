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


# Function to check if there is an account in the database
def account_exists(email, username, password):
    # Connect to the SQLite database

    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if an account exists with the given email, username, and password
    cursor.execute('''SELECT * FROM UserAccount 
                      WHERE email = ? AND username = ?''', 
                   (email, username))

    # Fetch the first row (if any)
    user = cursor.fetchone()
    if user:
        if api_utils.verify_password(cursor, user[0], password):
            # Close the connection
            db_utils.close(conn, cursor)
            return True
        else:
            # Close the connection
            db_utils.close(conn, cursor)
            return False

    else:
        # Return True if a matching account was found, False otherwise
        # Close the connection
        db_utils.close(conn, cursor)
        return False


@given('there exist the following user accounts')
def step_impl(context):
    # Call the setup function with the path
    setup_initial_accounts(DB_PATH)


@when('the user enters a valid email {validEmail}, a username {Username} and a secure password {validPassword}')
def valid_email(context, validEmail, Username, validPassword):
    #Request
    context.response = requests.put(f'{BASE_URL}/create_account', json={"email": validEmail, "username": Username, "password": validPassword})
    #Log if not the right status code
    if context.response.status_code != 201:
        error_msg = f'Expected 201 status code for valid creation, but got {context.response.status_code}.'
        logging.error(error_msg)
        error_msg = f'Got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)
    assert context.response.status_code == 201

@then('the account {validEmail} with username {Username} and password {validPassword} shall exist')
def account_shall_exist(context, validEmail, Username, validPassword):
    #Check if account exists
    expected_user_account = {
        "user_account_id": context.response.json()["user_account_id"],
        "email": validEmail,
        "username": Username,
    }
    assert "user_account_id" in context.response.json(), "Failed to retrieve user account ID"
    assert "email" in context.response.json(), "Failed to retrieve user account email"
    assert "username" in context.response.json(), "Failed to retrieve username"
    assert context.response.json() == expected_user_account, "Response does not match the expected user account"



@when('the user enters an invalid email {invalidEmail}, a username {Username} and a secure password {validPassword}')
def invalid_email(context, invalidEmail, Username, validPassword):
    context.email = invalidEmail
    context.username = Username
    context.password = validPassword
    context.response = requests.put(f'{BASE_URL}/create_account', json={"email": context.email, "username": context.username, "password": context.password})
    #Log if not the right status code
    if context.response.status_code != 409:
        error_msg = f'Expected 409 status code for invalid email, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg) 

@then('the account {invalidEmail} with username {Username} and password {validPassword} shall not exist because of an invalid email')
def no_exist_email(context, invalidEmail, Username, validPassword):
    #Check if account exists
    account_exists_result = account_exists( invalidEmail, Username, validPassword)
    #On false, print the message.
    assert not account_exists_result, f"Account with email '{invalidEmail}', username '{Username}', and password '{validPassword}' exists, but it shouldn't."

@then('an account shall not be created due to the email')
def account_not_created_email(context):
    #Check status code
    assert context.response.status_code == 409  # Assuming 409 is the status code for conflict (email already in use)



@when('the user enters a valid email {validEmail}, a username {Username} and an insecure password {invalidPassword}')
def invalid_password(context, validEmail, Username, invalidPassword):
    context.email = validEmail
    context.username = Username
    context.password = invalidPassword
    #Request
    context.response = requests.put(f'{BASE_URL}/create_account', json={"email": context.email, "username": context.username, "password": context.password})
    #Log if not the right status code
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for invalid password, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)

@then('the account {validEmail} with username {Username} and password {invalidPassword} shall not exist because of an invalid password')
def no_exist_password(context, validEmail, Username, invalidPassword):
    #Check if account exists
    account_exists_result = account_exists(validEmail, Username, invalidPassword)
    #On false, print the message
    assert not account_exists_result, f"Account with email '{validEmail}', username '{Username}', and password '{invalidPassword}' exists, but it shouldn't."

@then('an account shall not be created due to the password')
def account_not_created_password(context):
    #Check status code
    assert context.response.status_code == 400  # Assuming 400 is the status code for bad request (invalid password)


@when('the user enters a valid email {validEmail}, a username {Username} and no password')
def missing_password(context, validEmail, Username):
    context.email = validEmail
    context.username = Username
    context.password = ''

    # Send POST request to create an account with missing password
    context.response = requests.put(f'{BASE_URL}/create_account', json={"email": context.email, "username": context.username, "password": context.password})

@then('the account {validEmail} with username {Username} shall not exist because of a missing password field')
def missing_password_error(context, validEmail, Username):
    #Log if not the right status code
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for missing password, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)

    expected_message = "Missing required fields"
    if expected_message not in context.response.json()['error_msg']:
        error_msg = f'Expected error message "{expected_message}", but got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)
    

@when('the user enters no email, a username {Username} and a password {password}')
def missing_email(context, Username, password):
    context.email = ''
    context.username = Username
    context.password = password

    # Send POST request to create an account with missing email
    context.response = requests.put(f'{BASE_URL}/create_account', json={"email": context.email, "username": context.username, "password": context.password})

@then('the account {Username} with password {password} shall not exist because of a missing email field')
def missing_email_error(context, Username, password):
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for missing email, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)

    expected_message = "Missing required fields"
    if expected_message not in context.response.json()['error_msg']:
        error_msg = f'Expected error message "{expected_message}", but got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)

@when('the user enters a valid email {validEmail}, no username and a password {password}')
def missing_username(context, validEmail, password):
    context.email = validEmail
    context.username =''
    context.password = password

    # Send POST request to create an account with missing username
    context.response = requests.put(f'{BASE_URL}/create_account', json={"email": context.email, "username": context.username, "password": context.password})

@then('the account {validEmail} with password {password} shall not exist because of a missing username field')
def missing_username_error(context, validEmail, password):
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for missing username, but got {context.response.status_code}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)

    expected_message = "Missing required fields"
    if expected_message not in context.response.json()['error_msg']:
        error_msg = f'Expected error message "{expected_message}", but got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)
    





# Step Definitions for logging in successfully
@given('the user is on the login page')
def step_user_on_login_page(context):
    pass  # Implementation not required for API testing

@when('the user enters their email {email}')
def step_user_enters_email(context, email):
    context.email = email

@when('the user enters the password {password}')
def step_user_enters_new_password(context, password):
    context.password = password

@then('the user shall log in successfully')
def step_user_logs_in_successfully(context):
    context.response = requests.post(f'{BASE_URL}/login', json={"email": context.email, "password": context.password})
    #Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for successful login, but got {context.response.status_code}.'
        logging.error(error_msg)
        error_msg = context.response.json()['error_msg']
        logging.error(error_msg)
        raise AssertionError(error_msg)
    assert context.response.status_code == 200

@then('the system shall show the following message {message}')
def step_system_shows_success_message(context, message):
    response_data = context.response.json()
    print(response_data)
    assert response_data['message'] == message


# Step Definitions for logging in unsuccessfully
@then('the user shall not log in successfully')
def step_user_does_not_login_successfully(context):
    context.response = requests.post(f'{BASE_URL}/login', json={"email": context.email, "password": context.password})
    assert context.response.status_code != 200


@then('the system shall show the following error message {message}')
def step_system_shows_error_message(context, message):
    response_data = context.response.json()
    print(response_data)
    assert response_data['error_msg'] == message
