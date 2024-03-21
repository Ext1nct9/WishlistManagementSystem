import json
from behave import given, when, then
import requests
import sqlite3
from utils import db_utils, api_utils
from initialize_DB import DB_PATH


# Base URL for the API #
BASE_URL = "http://localhost:8000"
UP = "user_permission"
GET_UP = "get_user_permissions"

# Step Definitions #

# Background
@given("clear test data")
def up_clear_test_data(context):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Helper const
    IDS = [(i, ) for i in range(1, 13)]

    # Clear UserAccount
    cursor.executemany("DELETE FROM UserAccount WHERE user_account_id = ?;", IDS)

    # Clear Wishlist
    cursor.executemany("DELETE FROM Wishlist WHERE wishlist_id = ?;", IDS)

    # Clear UserPermission
    cursor.executemany("DELETE FROM UserPermission WHERE wishlist_id = ?;", IDS)

    # Commit and close connection
    db_utils.close(conn, cursor, True)

# Given
@given("there is a UserAccount with id {owner_user_id} and username {owner_username} and email {owner_email} and password {owner_password}")
def up_create_UserAccount(context, owner_user_id, owner_username, owner_email, owner_password):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Create UserAccount
    cursor.execute('''
        INSERT INTO UserAccount (user_account_id, username, email, password)
        VALUES (?, ?, ?, ?);
    ''', (owner_user_id, owner_username, owner_email, owner_password))

    # Commit and close connection
    db_utils.close(conn, cursor, True)

@given("there is a Wishlist with id {owner_wishlist_id} and name {owner_wishlist_name} and owner_id {owner_user_id}")
def up_create_Wishlist(context, owner_wishlist_id, owner_wishlist_name, owner_user_id):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Create Wishlist
    cursor.execute('''
        INSERT INTO Wishlist (wishlist_id, name, user_account_id)
        VALUES (?, ?, ?);
    ''', (owner_wishlist_id, owner_wishlist_name, owner_user_id))

    # Commit and close connection
    db_utils.close(conn, cursor, True)

@given("there is a UserPermission with wishlist_id {owner_wishlist_id} and user_id {other_user_id} and permissions {permissions}")
def up_create_UserPermission(context, owner_wishlist_id, other_user_id, permissions):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Create UserPermission
    cursor.execute('''
        INSERT INTO UserPermission (wishlist_id, user_account_id, permissions)
        VALUES (?, ?, ?);
    ''', (owner_wishlist_id, other_user_id, permissions))

    # Commit and close connection
    db_utils.close(conn, cursor, True)

# When
@when("the user with id {requester_id} attempts to add a new UserPermission with permissions {permissions} to the Wishlist with id {owner_wishlist_id} for the user with id {other_user_id}")
def up_attempt_to_create_UserPermission(context, requester_id, permissions, owner_wishlist_id, other_user_id):
    # Create request URL
    url = f"{BASE_URL}/{UP}/{other_user_id}/{owner_wishlist_id}"

    # Create cookies
    cookies = {"user_account_id": requester_id}

    # Create request body
    body = {
        "permissions": int(permissions)
    }

    # Make request
    context.response = requests.post(url, cookies=cookies, json=body)

@when("the user with id {requester_id} attempts to remove the UserPermission to the Wishlist with id {owner_wishlist_id} for the user with id {other_user_id}")
def up_attempt_to_delete_UserPermission(context, requester_id, owner_wishlist_id, other_user_id):
    # Create request URL
    url = f"{BASE_URL}/{UP}/{other_user_id}/{owner_wishlist_id}"

    # Create cookies
    cookies = {"user_account_id": requester_id}

    # Make request
    context.response = requests.delete(url, cookies=cookies)

@when("the user with id {owner_user_id} attempts to update the UserPermission to the Wishlist with id {owner_wishlist_id} for the user with id {other_user_id} to have permissions {new_permissions}")
def up_attempt_to_update_UserPermission(context, owner_user_id, owner_wishlist_id, other_user_id, new_permissions):
    # Create request URL
    url = f"{BASE_URL}/{UP}/{other_user_id}/{owner_wishlist_id}"

    # Create cookies
    cookies = {"user_account_id": owner_user_id}

    # Create request body
    body = {
        "permissions": int(new_permissions)
    }

    # Make request
    context.response = requests.put(url, cookies=cookies, json=body)

@when("the user with id {user_id} attempts to view all UserPermissions with wishlist_id {wishlist_id}")
def up_attempt_to_view_UserPermissions(context, user_id, wishlist_id):
    # Create request URL
    url = f"{BASE_URL}/{GET_UP}/{wishlist_id}"

    # Create cookies
    cookies = {"user_account_id": user_id}

    # Make request
    context.response = requests.get(url, cookies=cookies)

# Then
@then("the request returns the status code {status_code}")
def up_check_status_code(context, status_code):
    assert context.response.status_code == int(status_code)

@then("the response contains an error message")
def up_check_error_message(context):
    assert "error_msg" in context.response.json()

@then("there exists a UserPermission with wishlist_id {owner_wishlist_id} and user_id {other_user_id} and permissions {permissions}")
def up_check_UserPermission_exists1(context, owner_wishlist_id, other_user_id, permissions):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Query UserPermission
    cursor.execute('''
        SELECT * FROM UserPermission
        WHERE wishlist_id = ? AND user_account_id = ? AND permissions = ?;
    ''', (owner_wishlist_id, other_user_id, permissions))
    result = cursor.fetchone()

    # Check if UserPermission exists
    assert result is not None

    # Commit and close connection
    db_utils.close(conn, cursor, False)

@then("there exists a UserPermission with wishlist_id {owner_wishlist_id} and user_id {other_user_id}")
def up_check_UserPermission_exists2(context, owner_wishlist_id, other_user_id):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Query UserPermission
    cursor.execute('''
        SELECT * FROM UserPermission
        WHERE wishlist_id = ? AND user_account_id = ?;
    ''', (owner_wishlist_id, other_user_id))
    result = cursor.fetchone()

    # Check if UserPermission exists
    assert result is not None

    # Commit and close connection
    db_utils.close(conn, cursor, False)

@then("there does not exist a UserPermission with wishlist_id {wishlist_id} and user_id {user_id}")
def up_check_UserPermission_does_not_exist(context, wishlist_id, user_id):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Query UserPermission
    cursor.execute('''
        SELECT 0 FROM UserPermission
        WHERE wishlist_id = ? AND user_account_id = ?;
    ''', (wishlist_id, user_id))
    result = cursor.fetchone()

    # Check if UserPermission exists
    assert result is None

    # Commit and close connection
    db_utils.close(conn, cursor, False)

@then("the response is a list of size {size}")
def up_check_response_size(context, size):
    assert len(json.loads(context.response.text)) == int(size)

@then("the response is a list of UserPermissions that contains the UserPermission with wishlist_id {wishlist_id} and user_id {user_id} and permissions {permissions}")
def up_check_response_contains_UserPermission(context, wishlist_id, user_id, permissions):
    # Parse response
    response = json.loads(context.response.text)

    # Check if UserPermission exists in response
    assert {"wishlist_id": wishlist_id, "user_account_id": user_id, "permissions": int(permissions)} in response

# Cleanup
@then("delete the UserAccount with id {user_account_id}")
def up_delete_UserAccount(context, user_account_id):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Delete UserAccount
    cursor.execute('''
        DELETE FROM UserAccount
        WHERE user_account_id = ?;
    ''', (user_account_id,))

    # Commit and close connection
    db_utils.close(conn, cursor, True)

@then("delete the Wishlist with id {wishlist_id}")
def up_delete_Wishlist(context, wishlist_id):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Delete Wishlist
    cursor.execute('''
        DELETE FROM Wishlist
        WHERE wishlist_id = ?;
    ''', (wishlist_id,))

    # Commit and close connection
    db_utils.close(conn, cursor, True)

@then("delete the UserPermission with wishlist_id {wishlist_id} and user_id {user_id}")
def up_delete_UserPermission(context, wishlist_id, user_id):
    # Connect to DB
    conn, cursor = db_utils.conn()

    # Delete UserPermission
    cursor.execute('''
        DELETE FROM UserPermission
        WHERE wishlist_id = ? AND user_account_id = ?;
    ''', (wishlist_id, user_id))

    # Commit and close connection
    db_utils.close(conn, cursor, True)
