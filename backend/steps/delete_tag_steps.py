from behave import given, when, then
import requests
import sqlite3
from clean_DB import clean_data
from utils import db_utils, api_utils
from initialize_DB import DB_PATH

# Base URL for the API
BASE_URL = "http://localhost:8000/"

def tag_exists(tag_id):
    # Connect to the SQLite database
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if a tag exists with the given tag_id
    cursor.execute('''SELECT * FROM Tag 
                      WHERE tag_id = ? ''', 
                   (tag_id,))

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


@when ('the valid user {ValidAccountId} in wishlist {WishlistID} in tag {TagID} deletes the tag')
def step_impl(context, ValidAccountId, WishlistID, TagID):
    context.TagID = TagID
    # Delete the tag
    context.response = requests.delete(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', cookies ={"user_account_id": ValidAccountId})
    
    # Log if not the right status code
    if context.response.status_code != 204:
        error_msg = f'Expected 200 status code for valid tag deletion, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 204

@then ('the tag shall be deleted successfully')
def step_impl(context):
    # Check if the tag was deleted
    assert tag_exists(context.TagID) == False

@when ('the invalid user {InvalidAccountId} in wishlist {WishlistID} in tag {TagID} deletes the tag')
def step_impl(context, InvalidAccountId, WishlistID, TagID):
    context.TagID = TagID
    # Delete the tag
    context.response = requests.delete(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', cookies ={"user_account_id": InvalidAccountId})
    
    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid tag deletion, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403
    
@then ('the tag shall not be deleted')
def step_impl(context):
    # Check if the tag was deleted
    assert tag_exists(context.TagID) == True
    assert context.response.status_code != 204

@when ('the user with valid permission link {ValidPermissionLink} in wishlist {WishlistID} in tag {TagID} deletes the tag')
def step_impl(context, ValidPermissionLink, WishlistID, TagID):
    context.TagID = TagID
    # Delete the tag
    context.response = requests.delete(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', params={"link_permission_id": ValidPermissionLink})
    
    # Log if not the right status code
    if context.response.status_code != 204:
        error_msg = f'Expected 200 status code for valid tag deletion, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 204

@when ('the user with invalid permission link {InvalidPermissionLink} in wishlist {WishlistID} in tag {TagID} deletes the tag')
def step_impl(context, InvalidPermissionLink, WishlistID, TagID):
    context.TagID = TagID
    # Delete the tag
    context.response = requests.delete(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', params={"link_permission_id": InvalidPermissionLink})
    
    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid tag deletion, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403
