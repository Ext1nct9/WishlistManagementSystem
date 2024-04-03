from behave import given, when, then
import requests
import sqlite3
import logging
from clean_DB import clean_data
from utils import db_utils, api_utils
from initialize_DB import DB_PATH


# Base URL for the API
BASE_URL = "http://localhost:8000/"


def setup_initial_userPermission_to_view_wishlist(db_path):
    try:
        # Sample wishlist data
        userPermissions = [
            (1, 4, 0b00000001),
            (2, 2, 0b00000001),
            (3, 3, 0b00000001),
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

def setup_initial_linkPermission_to_view_wishlist(db_path):
    try:
        # Sample wishlist data
        linkPermissions = [
            (1, 2, 0b00000001),
            (2, 4, 0b00000001),
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

def retrieve_wishlist_from_database(wishlistId):
    conn, cursor = db_utils.conn()  # Assuming you have a function to create a database connection

    # Fetch wishlists from the database for the specified userAccountId
    cursor.execute('''
        SELECT wishlist_id, name, description, user_account_id
        FROM Wishlist
        WHERE wishlist_id = ?
    ''', (wishlistId,))

    wishlist = cursor.fetchone()

    # Close the database connection
    db_utils.close(conn, cursor)

    # Convert the result to a list of dictionaries for comparison
    return {
        "wishlist_id": wishlist[0],
        "name":wishlist[1],
        "description":wishlist[2],
        "user_account_id":wishlist[3],
    }


@given ('there exists user permissions to view by wishlist id')
def setup_user_permission_to_view(context):
    setup_initial_userPermission_to_view_wishlist(DB_PATH)       


@given ('there exists link permissions to view by wishlist id')
def setup_link_permission_to_view(context):
    setup_initial_linkPermission_to_view_wishlist(DB_PATH)   


@when ('the user {userId} with permission request to view a wishlist by wishlist id {wishlistId}')
def user_view_wishlist_by_wishlist_id(context, userId, wishlistId):

    # Request /wishlist/view/<string:wishlist_id>
    context.response = requests.get(f"{BASE_URL}wishlist/view/{wishlistId}", 
        json={"user_account_id": userId, "wishlist_id": wishlistId}, cookies={"user_account_id":userId})
    
    # Log if not the right status code
    if context.response.status_code != 200:
        error_message = (f"Expected status code 200, but got {context.response.status_code}")
        raise AssertionError(error_message)


@when ('the link {linkId} with permission request to view a wishlist by wishlist id {wishlistId}')
def link_view_wishlist_by_wishlist_id(context, linkId, wishlistId):

    # Request /wishlist/view/<string:wishlist_id>
    context.response = requests.get(f"{BASE_URL}wishlist/view/{wishlistId}?link_permission_id={linkId}", 
        json={"link_permission_id":linkId, "wishlist_id": wishlistId})
    
    # Log if not the right status code
    if context.response.status_code != 200:
        error_message = (f"Expected status code 200, but got {context.response.status_code}")
        raise AssertionError(error_message)
    

@then ('the wishlist name {name}, description {description} shall display by wishlist id {wishlistId}')
def show_wishlist_information(context, name, description, wishlistId):
    response = context.response

    # Ensure the response status code is 200
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Retrieve data from the database
    db_wishlist = retrieve_wishlist_from_database(wishlistId)

    # Check if the data in the response matches the data from the database
    assert response.json() == db_wishlist, f"Response data {response.json()} does not match database data {db_wishlist}"

    
@when ('the user {invalidUserId} requests to view a wishlist {wishlistId}')
def invalid_user_view_wishlist_by_wishlist_id(context, invalidUserId, wishlistId):

    # Request /wishlist/view/<string:wishlist_id>
    context.response = requests.get(f"{BASE_URL}wishlist/view/{wishlistId}", 
        json={"user_account_id": invalidUserId, "wishlist_id": wishlistId}, cookies={"user_account_id":invalidUserId})
    
    # Log if not the right status code
    if context.response.status_code != 403:
        error_message = (f"Expected status code 403, but got {context.response.status_code}")
        raise AssertionError(error_message)
    

@when ('the not logged-in user with link id {invalidLinkId} requests to view a wishlist {wishlistId}')
def invalid_link_view_wishlist_by_wishlist_id(context, invalidLinkId, wishlistId):

    # Request /wishlist/view/<string:wishlist_id>
    context.response = requests.get(f"{BASE_URL}wishlist/view/{wishlistId}?link_permission_id={invalidLinkId}", 
        json={"link_permission_id":invalidLinkId, "wishlist_id": wishlistId})
    
    # Log if not the right status code
    if context.response.status_code != 403:
        error_message = (f"Expected status code 403, but got {context.response.status_code}")
        raise AssertionError(error_message)

@when ('the user {userId} requests to view non-existing wishlist id {invalidWishlistId}')
def view_wishlist_by_non_exisiting_wishlist_id(context, userId, invalidWishlistId):

    # Request /wishlist/view/<string:wishlist_id>
    context.response = requests.get(f"{BASE_URL}wishlist/view/{invalidWishlistId}", 
        json={"user_account_id": userId, "wishlist_id": invalidWishlistId}, cookies={"user_account_id":userId})
    
    # Log if not the right status code
    if context.response.status_code != 404:
        error_message = (f"Expected status code 404, but got {context.response.status_code}")
        raise AssertionError(error_message)