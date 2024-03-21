from behave import *
from behave.runner import Context

import requests

from utils import api_utils, db_utils, db_procedures


@given('there is a user with username "{username}", email "{email}" and password "{password}"')
def given_there_is_a_user_with_username_email_and_password(
        context: Context,
        username: str,
        email: str,
        password: str
) -> None:
    # this test assumes login and register endpoints are functional

    print(f"Attempting to create user with username {username}, email {email} and password {password}...")

    attempt_create_account = requests.put(
        f'{api_utils.BASE_URL}/create_account',
        json={"email": email, "username": username, "password": password}
    )

    print(attempt_create_account.json())

    assert (attempt_create_account.status_code == 201  # if the user was created
            or attempt_create_account.status_code == 409)  # if the email is already in use

    if attempt_create_account.status_code == 409:
        print(f"User with email {email} already exists. Verifying credentials...")

        conn, cursor = db_utils.conn()

        # use direct db procedures to verify the user's credentials
        user = db_procedures.get_user_account_by_email(cursor, email)

        assert user['email'] == email, \
            f"Internal error: get_user_account_by_email returned wrong email: {user['email']} != {email}"

        assert api_utils.verify_password(cursor, user['user_account_id'], password), \
            f"Error: Password {password} does not match the password for the existing user with email {email}"

        conn.close()

        context.user_id = user['user_account_id']

    else:  # status code 201
        print(f"User with email {email} created successfully.")
        context.user_id = attempt_create_account.json()['user_account_id']

    context.email = email
    context.password = password

    print(f"User initialized successfully.")


@given('the user owns wishlist "{wishlist_id}" with name "{wishlist_name}"')
def given_the_user_owns_wishlist_with_name(
        context: Context,
        wishlist_id: str,
        wishlist_name: str
) -> None:
    # this test assumes user already exists, which should be covered by a previous step
    user_id = context.user_id

    # at the time of writing, api endpoints for creating and updating wishlists do not exist,
    # so we will use the database procedures directly
    print("Warning: Using database procedures directly to create/update wishlist")

    assert user_id is not None  # ensure the user exists

    description = None  # a field that is actually not needed for the test but required for the function

    conn, cursor = db_utils.conn()

    print(f"Verifying wishlist {wishlist_id} exists...")

    if db_procedures.verify_wishlist_exists(cursor, wishlist_id):
        print(f"Wishlist {wishlist_id} already exists. Overwriting the wishlist's data...")
        result = db_procedures.update_wishlist(cursor, wishlist_id, wishlist_name, description, user_id)

    else:
        print(f"Wishlist {wishlist_id} does not exist. Creating the wishlist...")
        result = db_procedures.create_wishlist_for_user(cursor, wishlist_id, wishlist_name, description, user_id)

    conn.commit()
    conn.close()

    returned_wishlist_id = result['wishlist_id']

    assert returned_wishlist_id == wishlist_id  # arbitrary check to ensure the wishlist was updated

    context.wishlist_id = wishlist_id

    print(f"Wishlist {wishlist_id} initialized successfully.")


@given("there is a permission link {other_link} for the wishlist with permission {other_permission}")
def given_there_is_a_permission_link_for_the_wishlist_with_permission(
        context: Context,
        other_link: str,
        other_permission: str
) -> None:
    # since we're testing the creation of permission links, avoid using the endpoint directly
    # instead, use the database procedures directly

    # this test assumes wishlist already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    # similarly, it should also assume that the user is logged in

    conn, cursor = db_utils.conn()

    print("Verifying the permission link exists...")

    if db_procedures.verify_link_permission_exists(cursor, other_link):
        print(f"The permission link already exists. Verifying the permission...")

        response = requests.get(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link/{other_link}")

        assert response.status_code == 200, f"Error: {response.json()}"

        if response.json()["permissions"] != int(other_permission, 2):
            print(f"Warning: the permission {other_link} already exists and has a different permission. "
                  f"Expected permissions to be {other_permission}, "
                  f"but got {response.json()['permissions']}.")

            print("Updating the permission...")

            result = db_procedures.update_link_permission(
                cursor,
                other_link,
                int(other_permission, 2)
            )

            link_permission_id = result['link_permission_id']

            assert link_permission_id == other_link, \
                (f"Internal Error:  update_link_permission returned a different link_permission_id. "
                 f"expected link_permission_id of the updated link to be {other_link}, "
                 f"but got {link_permission_id}.")
    else:
        print(f"The permission link does not exist. Creating permission link with permission {other_permission}...")

        result = db_procedures.create_link_permission_for_wishlist_with_link_permission_id(
            cursor,
            other_link,
            wishlist_id,
            int(other_permission, 2)
        )

        link_permission_id = result['link_permission_id']

        assert link_permission_id == other_link, \
            (f"Error: expected link_permission_id of the newly created link to be {other_link}, "
             f"but got {link_permission_id}.")

    conn.commit()
    conn.close()


@given("the user is logged in as owner of the wishlist")
def given_the_user_is_logged_in_as_owner_of_wishlist(context: Context) -> None:
    # this test assumes user and wishlist already exist, which should be covered by previous steps
    email = context.email
    password = context.password

    print(f"Logging in as user with email {email}...")

    response = requests.post(api_utils.BASE_URL + "/login", json={"email": email, "password": password})

    assert response.status_code == 200, f"Error: {response.json()}"

    print(f"Successfully logged in.")

    context.cookies = response.cookies.get_dict()  # persist cookies for the next steps


@given("the user is not logged in as owner of the wishlist")
def given_the_user_is_not_logged_in_as_owner_of_the_wishlist(context: Context) -> None:
    context.cookies = {}  # clear cookies


@then("the permission link {link_permission_id} is available")
def then_the_permission_link_other_link_is_available(context: Context, link_permission_id: str) -> None:
    # this test assumes wishlist already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    response = requests.get(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link/{link_permission_id}")

    assert response.status_code == 200, f"Error: {response.json()}"


@then("the permission link {link_permission_id} is not available")
def then_the_permission_link_link_permission_id_is_not_available(context: Context, link_permission_id: str) -> None:
    # this test assumes wishlist and permission link already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    response = requests.get(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link/{link_permission_id}")

    assert response.status_code > 299, \
        f"Error: expected operation to fail, but it didn't. {response.json()}"


@then("the permission link {link_permission_id} has permission {other_permission}")
def then_the_permission_link_other_link_has_permission_other_permission(
        context: Context,
        link_permission_id: str,
        other_permission: str
) -> None:
    # this test assumes wishlist already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    response = requests.get(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link/{link_permission_id}")

    assert response.status_code == 200, f"Error: {response.json()}"
    assert response.json()["permissions"] == int(other_permission, 2), \
        (f"Error: the permission {link_permission_id} has a different permission. "
         f"Expected permissions to be {other_permission}, "
         f"but got {response.json()['permissions']}.")


@then("the collaborators using the permission link {link_permission_id} has the permission {permission}")
def then_the_collaborators_using_the_permission_link_has_the_permission(
        context: Context,
        link_permission_id: str,
        permission: str
) -> None:
    # this test assumes wishlist and permission link already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    response = requests.get(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link/{link_permission_id}")

    assert response.status_code == 200, f"Error: {response.json()}"

    assert "permissions" in response.json(), \
        f"Error: The response does not contain an expected field 'permissions'."

    assert response.json()["permissions"] == int(permission, 2), \
        f"Error: expected permissions to be {int(permission, 2)}, but got {response.json()['permissions']}."


@then("the request should fail")
def then_the_request_should_fail(context: Context) -> None:
    response = context.response

    assert response.status_code > 299, \
        f"Error: expected operation to fail, but it didn't. {response.json()}"
