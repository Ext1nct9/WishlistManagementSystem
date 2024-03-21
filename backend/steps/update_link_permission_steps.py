from behave import *
from behave.runner import Context

import requests

from utils import api_utils, db_utils, db_procedures


@when("the user updates the permission link {link_permission_id} with permission {permission}")
def when_the_user_updates_the_permission_link_with_permission(
        context: Context,
        link_permission_id: str,
        permission: str
) -> None:
    # this test assumes wishlist and permission link already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    # similarly, it should also assume that the user is logged in
    cookies = context.cookies

    response = requests.put(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link/{link_permission_id}",
                            json={"permissions": int(permission, 2)},
                            cookies=cookies)

    context.response = response


@then("the permission link {link_permission_id} is updated with permission {permission}")
def then_the_permission_link_is_updated_with_permission(
        context: Context,
        link_permission_id: str,
        permission: str
) -> None:
    response = context.response

    assert response.status_code == 200, f"Error: {response.json()}"

    assert "link_permission_id" in response.json(), \
        f"Error: The response does not contain an expected field 'link_permission_id'."

    assert "permissions" in response.json(), \
        f"Error: The response does not contain an expected field 'permissions'."

    assert response.json()["permissions"] == int(permission, 2), \
        f"Error: expected permissions to be {int(permission, 2)}, but got {response.json()['permissions']}."
