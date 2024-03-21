from behave import *
from clean_DB import clean_data
from initialize_DB import DB_PATH
from utils import api_utils, db_utils

import requests
import sqlite3

# Base URL for the API
BASE_URL = "http://localhost:8000/"


def setup_initial_accounts():
    try:
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


def setup_initial_wishlists():
    try:
        # Sample wishlist data
        wishlists = [
            (123, "Dress", "dresses for me", 1)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial wishlists
        cursor.executemany('''INSERT INTO Wishlist (wishlist_id, name, description, user_account_id)
                          VALUES (?, ?, ?, ?)''', wishlists)

        # Commit changes and close the connection
        conn.commit()
        print("Initial wishlists set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial accounts: {e}")

    db_utils.close(conn, cursor)


def setup_initial_items():
    try:
        # Sample item data
        items = [
            (546, "Pencil", "For writing", "link data", 1, 1, 123),
        ]

        conn, cursor = db_utils.conn()

        # Insert initial items
        cursor.executemany('''INSERT INTO Item (item_id, name, description, link, status, rank, wishlist_id)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', items)

        # Commit changes and close the connection
        conn.commit()
        print("Initial items set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial items: {e}")

    db_utils.close(conn, cursor)


def setup_initial_userPermission(permissions):
    try:
        # Sample wishlist data
        userPermissions = [
            (1, 123, permissions),
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


@given('the user has permission to comment {i:w}')
def step_impl(context, i):
    setup_initial_userPermission(0b00111111)


@given('the user does not have permission to comment 123')
def step_impl(context):
    setup_initial_userPermission(0)


@given('the wishlist {w} has an item {i}')
def step_impl(context, w, i):
    clean_data(DB_PATH)
    setup_initial_wishlists()
    setup_initial_items()


@when('the user writes a comment in {i}')
def step_impl(context, i):
    response = requests.post(BASE_URL + f"comment/{i}", json={"body": "test comment"}, cookies={"user_account_id": "1"})
    context.response = response


@when('the user writes an empty comment in {i}')
def step_impl(context, i):
    response = requests.post(BASE_URL + f"comment/{i}", json={"body": None}, cookies={"user_account_id": "1"})
    context.response = response


@then('the comment is recorded in the system')
def step_impl(context):
    assert context.response.status_code == 201
    comment_id = context.response.json()["comment_id"]
    conn, cursor = db_utils.conn()
    cursor.execute('''
            SELECT comment_id
            FROM Comment
            WHERE comment_id = ?
        ''', (comment_id,))
    comment = cursor.fetchone()
    db_utils.close(conn, cursor)
    assert comment is not None


@then('the comment is not recorded in the system')
def step_impl(context):
    assert context.response.status_code != 201


@then('the comment is automatically assigned a username and ID')
def step_impl(context):
    assert context.response.json()["user_info"] is not None and context.response.json()["comment_id"] is not None


@then('there is an error message {e}')
def step_impl(context, e):
    assert 400 <= context.response.status_code <= 599
    assert context.response.json()["error_msg"] == e
