import sqlite3

import requests
from behave import given, when, then

from clean_DB import clean_data
from initialize_DB import DB_PATH
from utils import api_utils, db_utils

# Base URL for the API
BASE_URL = "http://localhost:8000/"

@when('the valid user {ValidAccountId} in wishlist {WishlistID} in tag {TagID} enters a valid label {Label}, and a color {Color} to update the tag')
def step_impl(context, ValidAccountId, WishlistID, TagID, Label, Color):
    context.wishlist_id = WishlistID
    # Update the tag
    context.response = requests.post(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', json={"label": Label, "color": Color}, cookies ={"user_account_id": ValidAccountId})
    
    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 201 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200

@then('the tag {TagID} shall be updated to have label {Label} and color {Color}')
def step_impl(context, TagID, Label, Color):
    # Check if the tag was updated
    expected_response = {"tag_id": TagID, 
                         "label": Label, 
                         "color": Color, 
                         "wishlist_id": context.wishlist_id}
    assert context.response.json() == expected_response

@when('the valid user {ValidAccountId} in wishlist {WishlistID} in tag {TagID} enters a valid label {Label}, and no color to update the tag')
def step_impl(context, ValidAccountId, WishlistID, TagID, Label):
    context.wishlist_id = WishlistID
    # Update the tag
    context.response = requests.post(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', json={"label": Label}, cookies ={"user_account_id": ValidAccountId})
    
    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 201 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200

@then('the tag {TagID} shall be updated to have label {Label} and a random color')
def step_impl(context, TagID, Label):
    # Check if the tag was updated
    expected_response = {"tag_id": TagID, 
                         "label": Label, 
                         "color": context.response.json()["color"], 
                         "wishlist_id": context.wishlist_id}
    assert context.response.json()['color'] != None
    assert context.response.json() == expected_response

@when('the valid user {ValidAccountId} in wishlist {WishlistID} in tag {TagID} enters no label, and a color {Color} to update the tag')
def step_impl(context, ValidAccountId, WishlistID, TagID, Color):
    context.wishlist_id = WishlistID
    # Update the tag
    context.response = requests.post(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', json={"color": Color}, cookies ={"user_account_id": ValidAccountId})
    
    # Log if not the right status code
    if context.response.status_code != 400:
        error_msg = f'Expected 400 status code for invalid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 400

@then('the tag shall not be updated')
def step_impl(context):
    # Check if the tag was not updated
    assert context.response.status_code != 200

@when('the invalid user {InvalidAccountId} in wishlist {WishlistID} in tag {TagID} enters a valid label {Label}, and a color {Color} to update the tag')
def step_impl(context, InvalidAccountId, WishlistID, TagID, Label, Color):
    context.wishlist_id = WishlistID
    # Update the tag
    context.response = requests.post(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', json={"label": Label, "color": Color}, cookies ={"user_account_id": InvalidAccountId})
    
    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403

@when('the user with valid permission link {ValidPermissionLink} in wishlist {WishlistID} in tag {TagID} enters a valid label {Label}, and a color {Color} to update the tag')
def step_impl(context, ValidPermissionLink, WishlistID, TagID, Label, Color):
    context.wishlist_id = WishlistID
    # Update the tag
    context.response = requests.post(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', json={"label": Label, "color": Color}, params={"link_permission_id": ValidPermissionLink})
    
    # Log if not the right status code
    if context.response.status_code != 200:
        error_msg = f'Expected 201 status code for valid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 200

@when('the user with invalid permission link {InvalidPermissionLink} in wishlist {WishlistID} in tag {TagID} enters a valid label {Label}, and a color {Color} to update the tag')
def step_impl(context, InvalidPermissionLink, WishlistID, TagID, Label, Color):
    context.wishlist_id = WishlistID
    # Update the tag
    context.response = requests.post(f'{BASE_URL}/wishlist/{WishlistID}/tags/{TagID}', json={"label": Label, "color": Color}, params={"link_permission_id": InvalidPermissionLink})
    
    # Log if not the right status code
    if context.response.status_code != 403:
        error_msg = f'Expected 403 status code for invalid wishlist update, but got {context.response.status_code}.'
        raise AssertionError(error_msg)
    assert context.response.status_code == 403
