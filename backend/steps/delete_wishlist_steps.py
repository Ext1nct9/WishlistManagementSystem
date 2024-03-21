from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils
from initialize_DB import DB_PATH


# Base URL for the API
BASE_URL = "http://localhost:8000/"

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
def wishlist_exists (wishlist_id):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a wishlist exists with the given wishlist_id
    cursor.execute('''SELECT * FROM Wishlist 
                      WHERE wishlist_id = ? ''', 
                   (wishlist_id))

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

    
# Scenario 1 - Successful deletion of a wishlist
@when('the user {userAccountId} request to delete a valid wishlist {wishlist_id}')
def user_requests_to_delete_wishlist(context, userAccountId, wishlist_id):
    
    # Request 
    context.response = requests.delete(f"{BASE_URL}wishlist/delete/{wishlist_id}", cookies={"user_account_id":userAccountId})
    
    # Log if not the right status code
    
    if context.response.status_code != 204:
        error_message = (f"Expected status code 204, but got {context.response.status_code}")
        raise AssertionError(error_message)

@then('the wishlist {wishlist_id} with name {name}, and description {description} shall not exist under {userAccountId} anymore.')
def user_deletes_wishlist(context, wishlist_id, name, description, userAccountId):
    assert not wishlist_exists(wishlist_id)




# Scenario 2 - Unsuccessful deletion of a wishlist (invalid wishlist id)

@when('the user {userAccountId} request to delete an invalid wishlist {inValidwishlistId}.')
def user_requests_to_delete_wishlist(context, userAccountId, inValidwishlistId):

    # Request
    context.response = requests.delete(f"{BASE_URL}wishlist/delete/{inValidwishlistId}", cookies={"user_account_id":userAccountId})

    # Log if not the right status code
    if context.response.status_code != 404:
        error_message = (f"Expected status code 404, but got {context.response.status_code}")
        raise AssertionError(error_message)
    else:
        context.response.status_code == 404


# Scenario 3 - Unsuccessful deletion of a wishlist (non-owner user account id)

@when ('the non-owner {invalidUserAccountId} attempts to delete the wishlist with ID {validwishlistId}')
def non_owner_attempt_to_delete_wishlist(context, invalidUserAccountId, validwishlistId):

    # Request
    context.response = requests.delete(f"{BASE_URL}wishlist/delete/{validwishlistId}", cookies={"user_account_id":invalidUserAccountId})

    # Log if not the right status code
    if context.response.status_code != 403:
        error_message = (f"Expected status code 403, but got {context.response.status_code}")
        raise AssertionError(error_message)
    else:
        context.response.status_code == 403

