from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils, db_procedures
from initialize_DB import DB_PATH

# Base URL for the API
BASE_URL = "http://localhost:8000/"

def retrieve_wishlists_from_database(userAccountId):
    conn, cursor = db_utils.conn()  # Assuming you have a function to create a database connection

    # Fetch wishlists from the database for the specified userAccountId
    cursor.execute('''
        SELECT wishlist_id, name, description
        FROM Wishlist
        WHERE user_account_id = ?
    ''', (userAccountId,))

    db_wishlists = cursor.fetchall()

    # Close the database connection
    db_utils.close(conn, cursor)

    # Convert the result to a list of dictionaries for comparison
    return [{
        "wishlist_id": wishlist[0],
        "name": wishlist[1],
        "description": wishlist[2]
    } for wishlist in db_wishlists]


# to check the wishlists' data
def log_existing_wishlists(user_account_id, wishlists):
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
    logging.info(f'Wishlists from API response for user_account_id {user_account_id}: {wishlists}')

    # Close the connection
    db_utils.close(conn, cursor)

@when('the user {userAccountId} requests to view all the wishlists')
def step_when_user_requests_wishlists(context, userAccountId):
    context.user_account_id = userAccountId
    context.response = requests.get(f'{BASE_URL}/wishlist/view_by_user/{userAccountId}', cookies={"user_account_id":userAccountId})

    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for successful request, but got {context.response.status_code}.'
        logging.error(error_msg)
        error_msg = f'Got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)


@when('the user {userAccountId} with invalid account id requests to view all wishlists')
def step_when_user_requests_wishlists_invalid(context, userAccountId):
    context.user_account_id = userAccountId
    context.response = requests.get(f'{BASE_URL}/wishlist/view_by_user/{userAccountId}', cookies={"user_account_id":userAccountId})

    if context.response.status_code != 404:
        error_msg = f'Expected 404 status code for unsuccessful request, but got {context.response.status_code}.'
        logging.error(error_msg)
        error_msg = f'Got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)


@when ('the user {userAccountId} with account id requests to view wishlists')
def step_no_wishlist (context, userAccountId):
    context.user_account_id = userAccountId
    context.response = requests.get(f'{BASE_URL}/wishlist/view_by_user/{context.user_account_id}', cookies={"user_account_id":context.user_account_id})

    if context.response.status_code != 404:
        error_msg = f'Expected 404 status code for unsuccessful request, but got {context.response.status_code}.'
        logging.error(error_msg)
        error_msg = f'Got {context.response.json()["error_msg"]}.'
        logging.error(error_msg)
        raise AssertionError(error_msg)


@then('all the wishlists in the database for user {userAccountId} match the query result')
def step_then_check_wishlist_details(context, userAccountId):
    response = context.response

    user_wishlists = response.json()
    assert user_wishlists, "No wishlists returned in the response"

    # Retrieve wishlists from the database for the specified userAccountId
    db_wishlists = retrieve_wishlists_from_database(userAccountId)

    # Log existing wishlists after retrieving wishlists from the database
    log_existing_wishlists(userAccountId, db_wishlists)

    # Compare the retrieved wishlists with the user_wishlists from the API response
    assert len(user_wishlists) == len(db_wishlists), "Number of wishlists does not match"

    for wishlist in user_wishlists:
        # Check if the wishlist from the API response is present in the database wishlists
        assert wishlist in db_wishlists, f"Wishlist {wishlist} not found in the database"

    
