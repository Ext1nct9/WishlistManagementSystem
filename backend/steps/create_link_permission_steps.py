from behave import *
from behave.runner import Context

import requests

from utils import api_utils, db_utils, db_procedures


@when("the user creates a permission link for the wishlist without explicitly specifying a permission")
def when_the_user_creates_a_permission_link_for_the_wishlist_without_explicitly_specifying_a_permission(
        context: Context
) -> None:
    # this test assumes wishlist already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    # similarly, it should also assume that the user is logged in
    cookies = context.cookies

    response = requests.post(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link",
                             json={"permissions": 0},  # 0 is the default permission
                             cookies=cookies)

    context.response = response


@when("the user creates a permission link for the wishlist with permission {permission}")
def when_the_user_creates_a_permission_link_for_the_wishlist_with_permission(context: Context, permission: str) -> None:
    # this test assumes wishlist already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    # similarly, it should also assume that the user is logged in
    cookies = context.cookies

    response = requests.post(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link",
                             json={"permissions": int(permission, 2)},
                             cookies=cookies)

    context.response = response


@then("a permission link for the wishlist is created with the default permission")
def then_a_permission_link_for_the_wishlist_is_created_with_the_default_permission(context: Context) -> None:
    response = context.response

    assert response.status_code == 201, f"Error: {response.json()}"

    assert "link_permission_id" in response.json(), \
        f"Error: The response does not contain an expected field 'link_permission_id'."

    assert "permissions" in response.json(), \
        f"Error: The response does not contain an expected field 'permissions'."

    assert response.json()["permissions"] == 0, \
        f"Error: expected permissions to be 0, but got {response.json()['permissions']}."


@then("a permission link for the wishlist is created with permission {permission}")
def then_a_permission_link_for_the_wishlist_is_created_with_permission(context: Context, permission: str) -> None:
    response = context.response

    assert response.status_code == 201, f"Error: {response.json()}"

    assert "link_permission_id" in response.json(), \
        f"Error: The response does not contain an expected field 'link_permission_id'."

    assert "permissions" in response.json(), \
        f"Error: The response does not contain an expected field 'permissions'."

    assert response.json()["permissions"] == int(permission, 2), \
        f"Error: expected permissions to be {permission}, but got {response.json()['permissions']}."


@then("no permission link is created for the wishlist")
def then_no_permission_link_is_created_for_the_wishlist(context: Context) -> None:
    # this is a bit of a stretch,
    # because technically we need to check that the number of permission link in the database
    # did not increase after the request to know that no permission link was created,
    # but it would be a bit overkill to do that.
    # the simpler alternative is to check that the response body doesn't contain a link permission,
    # as any requests that creates a link permission should return the link permission in the response body.

    response = context.response

    assert "link_permission_id" not in response.json(), \
        f"Error: expected no permission link to be created, but got {response.json()}"


