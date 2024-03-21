from behave import *
from behave.runner import Context

import requests

from utils import api_utils, db_utils, db_procedures


@when("the user revokes the permission link {link_permission_id}")
def when_the_user_revokes_the_permission_link(context: Context, link_permission_id: str) -> None:
    # this test assumes wishlist and permission link already exist, which should be covered by previous steps
    wishlist_id = context.wishlist_id

    # similarly, it should also assume that the user is logged in
    cookies = context.cookies

    response = requests.delete(f"{api_utils.BASE_URL}/wishlist/{wishlist_id}/permission_link/{link_permission_id}",
                               cookies=cookies)

    context.response = response


@then("the collaborators using the permission link {link_permission_id} lose access to the wishlist")
def then_the_collaborators_using_the_permission_link_lose_access_to_the_wishlist(
        context: Context,
        link_permission_id: str
) -> None:
    response = requests.get(f"{api_utils.BASE_URL}/wishlist/{context.wishlist_id}/permission_link/{link_permission_id}")

    assert response.status_code == 404,\
        f"Expected permission link {link_permission_id} to be revoked, but it still exists."
