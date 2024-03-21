from behave import *
from clean_DB import clean_data
from initialize_DB import DB_PATH
from utils import api_utils, db_utils

import requests
import sqlite3

# Base URL for the API
BASE_URL = "http://localhost:8000/"


def setup_initial_comments(comment_id, item):
    try:
        # Sample comment data
        comments = [
            (comment_id, 1, True, "test comment", item)
        ]

        conn, cursor = db_utils.conn()

        # Insert initial comments
        cursor.executemany('''INSERT INTO Comment (comment_id, user_info, is_account, body, item_id)
                          VALUES (?, ?, ?, ?, ?)''', comments)

        # Commit changes and close the connection
        conn.commit()
        print("Initial comments set up successfully.")

    except sqlite3.Error as e:
        print(f"Error setting up initial comments: {e}")

    db_utils.close(conn, cursor)

@given('the user is owner of comment {comment_id} on {item}')
def step_impl(context, comment_id, item):
    setup_initial_comments(comment_id, item)


@when('the user deletes comment {comment_id}')
def step_impl(context, comment_id):
    response = requests.delete(BASE_URL + f'comment/{comment_id}', cookies={"user_account_id": "1"})
    context.response = response


@then('the comment {comment_id} is removed from the database')
def step_impl(context, comment_id):
    conn, cursor = db_utils.conn()
    cursor.execute('''
            SELECT comment_id
            FROM Comment
            WHERE comment_id = ?
        ''', (comment_id,))
    comment = cursor.fetchone()
    db_utils.close(conn, cursor)
    assert comment is None
