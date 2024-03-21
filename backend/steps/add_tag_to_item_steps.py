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
        # Initialize mock database
        clean_data(db_path)
        user_accounts = [
            (1, 'whamuzi@gmail.com', 'MrReborn', api_utils.hash_password('Abcdefghi1')),
            (2, 'mawpiew@gmail.com', 'Lost Boy', api_utils.hash_password('VixxenBibi#1')),
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


def setup_initial_wishlists(db_path):
    try:
        # Sample wishlist
        wishlist = (1, 'Trip to Italy', 'Graduation gift', 2)
        conn, cursor = db_utils.conn()
        cursor.execute('''INSERT INTO Wishlist (wishlist_id, name, description, user_account_id)
            VALUES (?, ?, ?, ?)
            ''', wishlist)
        # Commit changes and close the connection
        conn.commit()
        print("Initial wishlist set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial wishlist: {e}")
    
    db_utils.close(conn, cursor)


def setup_initial_tags(db_path):
    try:
        # Sample tags
        tags = [
            (1, 'clothes', 'blue', 1),
            (2, 'essentials', 'pink', 1),
            (3, 'medical', 'red', 1)
        ]
        conn, cursor = db_utils.conn()

        cursor.executemany('''INSERT INTO Tag (tag_id, label, color, wishlist_id)
            VALUES (?, ?, ?, ?)
            ''', tags)
        # Commit changes and close the connection
        conn.commit()
        print("Initial tags set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial tags: {e}")
    
    db_utils.close(conn, cursor)


def setup_initial_items(db_path):
    try:
        # Sample items
        items = [
            (1, 'bathing suit', 'to swim', 'decathlon.com', 'pending', 1, 1),
            (2, 'sunscreen', 'to protect myself', 'pharmaprix.com', 'pending', 2, 1)
        ]
        conn, cursor = db_utils.conn()
        cursor.executemany('''INSERT INTO Item (item_id, name, description, link, status, rank, wishlist_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', items)
        # Commit changes and close the connection
        conn.commit()
        print("Initial items set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial items: {e}")
    
    db_utils.close(conn, cursor)


def setup_initial_itemTags(db_path):
    try:
        # Sample itemTags
        itemTag = (1, 1)
        conn, cursor = db_utils.conn()
        cursor.execute('''INSERT INTO ItemTag (tag_id, item_id) VALUES (?, ?)
                ''', itemTag)
        # Commit changes and close the connection
        conn.commit()
        print("Initial itemTags set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial itemTags: {e}")
    
    db_utils.close(conn, cursor)


# Function to check if there is an itemTag in the database
def itemTag_exists(item_id, tag_id):
    # Create a cursor for database operations
    conn, cursor = db_utils.conn()

    # Execute a SELECT query to check if an itemTag exists with the given item_id and tag_id
    cursor.execute('''SELECT * FROM ItemTag 
                      WHERE item_id = ? AND tag_id = ?''', 
                   (item_id, tag_id))

    # Fetch the first row (if any)
    itemTag = cursor.fetchone()
    if itemTag:
        db_utils.close(conn, cursor)
        return True

    # Return True if a matching account was found, False otherwise
    db_utils.close(conn, cursor)
    return False


# Background


@given('there exist the following accounts')
def accounts_imp(context):
    # Call the setup function with the path
    setup_initial_accounts(DB_PATH)

@given('there is a wishlist')
def wishlists_impl(context):
    # Call the setup function with the path
    setup_initial_wishlists(DB_PATH)

@given('there exist the following tags in the wishlist')
def tags_impl(context):
    # Call the setup function with the path
    setup_initial_tags(DB_PATH)

@given('there exist the following items in the wishlist')
def items_impl(context):
    # Call the setup function with the path
    setup_initial_items(DB_PATH)

@given('there exist the following items with the following tags in the wishlist')
def itemTags_impl(context):
    # Call the setup function with the path
    setup_initial_itemTags(DB_PATH)


# Add a tag to an item successfully

@given('the user {email}, {password} has the permission to assign tags to items')
def is_logged_in_with_permission(context, email, password):
    # Make a request to the login endpoint to authenticate the user
    context.response = requests.post(f'{BASE_URL}/login', json={"email": email, "password": password})
    context.auth_cookie = context.response.cookies.get('user_account_id')
    logging.info(context.response.text)
    assert context.response.status_code == 200, "Login failed"

@when('the user adds a tag {tagToAdd} to the item {item} in wishlist {wishlist}')
def successful_add_tag_to_item(context, tagToAdd, item, wishlist):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.post(f'{BASE_URL}/add_tag_to_item', json={"item_id": item, "tag_id": tagToAdd, "wishlist_id": wishlist}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 200 status code for valid adding tag to item, but got {context.response.status_code}.'
        logging.info(context.response.text)
        raise AssertionError(error_msg)
    assert context.response.status_code == 200


@then('the itemTag {item}, {tagToAdd} shall exist')
def itemTag_shall_exist(context, item, tagToAdd):
    assert itemTag_exists(item, tagToAdd)


# Add tag to item unsuccessfully

@given('the user {email}, {password} does not have the permission to assign tags to items')
def is_logged_in_with_no_permission(context, email, password):
    # Make a request to the login endpoint to authenticate the user
    context.response = requests.post(f'{BASE_URL}/login', json={"email": email, "password": password})
    context.auth_cookie = context.response.cookies.get('user_account_id')
    assert context.response.status_code == 200, "Login failed"


@when('the user attempts to add a tag {tagToAdd} to the item {item} in wishlist {wishlist}')
def unsuccessful_add_tag_to_item(context, tagToAdd, item, wishlist):
    # Request
    cookies = {'user_account_id' : context.auth_cookie}
    context.response = requests.post(f'{BASE_URL}/add_tag_to_item', json={"item_id": item, "tag_id": tagToAdd, "wishlist_id": wishlist}, cookies=cookies)

    # Log if not the right status code
    if context.response.status_code == 200:
        error_msg = f'Unexpected 200 status code for invalid add tag to item.'
        raise AssertionError(error_msg)


@then('the itemTag {item}, {tagToAdd} shall not exist')
def itemTag_shall_not_exist(context, item, tagToAdd):
    assert not itemTag_exists(item, tagToAdd)


@then('the system shall raise the error {error}')
def step_system_shows_error_message(context, error):
    response_data = context.response.json()
    print(response_data)
    assert response_data['error_msg'] == error
