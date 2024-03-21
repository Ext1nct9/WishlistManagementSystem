from sqlite3 import Cursor
from typing import Any

from . import api_utils


def verify_wishlist_exists(cursor, wishlist_id) -> bool:
    cursor.execute('''
                SELECT wishlist_id
                FROM Wishlist
                WHERE wishlist_id = ?
            ''', (wishlist_id,))
    return cursor.fetchone() is not None
    # return {"error_msg": "The target Wishlist does not exist."}, 400


def verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id) -> bool:
    cursor.execute('''
                SELECT user_account_id
                FROM Wishlist
                WHERE wishlist_id = ?
            ''', (wishlist_id,))
    wishlist_owner_id = cursor.fetchone()[0]
    return wishlist_owner_id == requester_id
    # return {"error_msg": "You do not have permission to create a UserPermission for this Wishlist."}, 403


def verify_requester_is_owner_of_comment(cursor, comment_id, requester_id) -> bool:
    cursor.execute('''
                SELECT user_info
                FROM Comment
                WHERE comment_id = ?
            ''', (comment_id,))
    comment_owner_id = cursor.fetchone()[0]
    return comment_owner_id == requester_id
    # return {"error_msg": "You do not have permission to create a UserPermission for this Wishlist."}, 403


def verify_link_permission_exists(cursor, link_permission_id) -> bool:
    cursor.execute('''
                SELECT link_permission_id
                FROM LinkPermission
                WHERE link_permission_id = ?
            ''', (link_permission_id,))
    return cursor.fetchone() is not None


def verify_user_account_exists(cursor, user_account_id) -> bool:
    cursor.execute('''
        SELECT 0
        FROM UserAccount
        WHERE user_account_id = ?
    ''', (user_account_id,))
    return cursor.fetchone() is not None


def get_all_user_permissions_for_wishlist(cursor, wishlist_id) -> list[dict[str, Any]]:
    cursor.execute('''
        SELECT
            wishlist_id,
            user_account_id,
            permissions
        FROM UserPermission
        WHERE wishlist_id = ?
    ''', (wishlist_id,))

    user_permissions = cursor.fetchall()

    return [{
        "wishlist_id": user_permission[0],
        "user_account_id": user_permission[1],
        "permissions": user_permission[2]
    } for user_permission in user_permissions]

def verify_user_permission_exists(cursor, user_account_id, wishlist_id) -> bool:
    cursor.execute('''
        SELECT 0
        FROM UserPermission
        WHERE user_account_id = ?
        AND wishlist_id = ?
    ''', (user_account_id, wishlist_id,))
    return cursor.fetchone() is not None


def get_user_account_by_email(cursor: Cursor, email: str) -> dict[str, Any]:
    cursor.execute('''
        SELECT user_account_id, email, username, password, pfp
        FROM UserAccount
        WHERE email = ?
    ''', (email,))
    user_account = cursor.fetchone()

    return {
        "user_account_id": user_account[0],
        "email": user_account[1],
        "username": user_account[2],
        "password": user_account[3],
        "pfp": user_account[3]
    }


def get_link_permission(cursor: Cursor, link_permission_id: str) -> dict[str, Any]:
    cursor.execute('''
        SELECT link_permission_id, permissions, wishlist_id
        FROM LinkPermission
        WHERE link_permission_id = ?
    ''', (link_permission_id,))
    link_permission = cursor.fetchone()

    return {
        "link_permission_id": link_permission[0],
        "permissions": link_permission[1],
        "wishlist_id": link_permission[2]
    }


def get_all_link_permissions_for_wishlist(cursor: Cursor, wishlist_id: str) -> list[dict[str, Any]]:
    cursor.execute('''
                            SELECT link_permission_id, permissions
                            FROM LinkPermission
                            WHERE wishlist_id = ?
                        ''', (wishlist_id,))

    permission_links = cursor.fetchall()

    return [{
        "link_permission_id": link_permission[0],
        "permissions": link_permission[1]
    } for link_permission in permission_links]


def create_wishlist_for_user(
        cursor: Cursor,
        wishlist_id: str,
        name: str,
        description: str,
        user_account_id: str
) -> dict[str, Any]:
    cursor.execute('''
        INSERT INTO Wishlist (wishlist_id, name, description, user_account_id)
        VALUES (?, ?, ?, ?)
        RETURNING *
    ''', (wishlist_id, name, description, user_account_id,))

    new_wishlist = cursor.fetchone()

    return {
        "wishlist_id": new_wishlist[0],
        "name": new_wishlist[1],
        "description": new_wishlist[2],
        "user_account_id": new_wishlist[3]
    }


def update_wishlist(
        cursor: Cursor,
        wishlist_id: str,
        name: str,
        description: str,
        user_account_id: str
) -> dict[str, Any]:
    cursor.execute('''
        UPDATE Wishlist
        SET name = ?, description = ?, user_account_id = ?
        WHERE wishlist_id = ?
        RETURNING *
    ''', (name, description, user_account_id, wishlist_id))

    updated_wishlist = cursor.fetchone()

    return {
        "wishlist_id": updated_wishlist[0],
        "name": updated_wishlist[1],
        "description": updated_wishlist[2],
        "user_account_id": updated_wishlist[3]
    }


def delete_wishlist(cursor: Cursor, wishlist_id: str) -> dict[str, Any]:
    cursor.execute('''
        DELETE FROM Wishlist
        WHERE wishlist_id = ?
        RETURNING *
    ''', (wishlist_id,))

    deleted_wishlist = cursor.fetchone()

    return {
        "wishlist_id": deleted_wishlist[0],
        "name": deleted_wishlist[1],
        "description": deleted_wishlist[2],
        "user_account_id": deleted_wishlist[3]
    }


def create_link_permission_for_wishlist(cursor: Cursor, wishlist_id: str, permissions: int) -> dict[str, Any]:
    # assign a random UUID to the new LinkPermission
    link_permission_id = api_utils.generate_id()
    valid_uuid = False

    for _ in range(5):
        # check for clashes
        if verify_link_permission_exists(cursor, link_permission_id):
            # reassign a random UUID to the new LinkPermission
            link_permission_id = api_utils.generate_id()
        else:
            valid_uuid = True
            break

    # technically, it would never happen for the time of the universe
    # that the loop would run 5 times and still not find a unique UUID.
    # but just in case, we have a failsafe.

    if not valid_uuid:
        raise Exception("Could not generate a unique UUID for the new LinkPermission.")

    cursor.execute('''
    INSERT INTO LinkPermission (link_permission_id, permissions, wishlist_id)
    VALUES (?, ?, ?)
    RETURNING *
                ''', (link_permission_id, permissions, wishlist_id,))

    link_permission = cursor.fetchone()

    return {
        "link_permission_id": link_permission[0],
        "permissions": link_permission[1],
        "wishlist_id": link_permission[2]
    }


def create_link_permission_for_wishlist_with_link_permission_id(
        cursor: Cursor,
        link_permission_id: str,
        wishlist_id: str,
        permissions: int
) -> dict[str, Any]:
    cursor.execute('''
    INSERT INTO LinkPermission (link_permission_id, permissions, wishlist_id)
    VALUES (?, ?, ?)
    RETURNING *
    ''', (link_permission_id, permissions, wishlist_id,))

    link_permission = cursor.fetchone()

    return {
        "link_permission_id": link_permission[0],
        "permissions": link_permission[1],
        "wishlist_id": link_permission[2]
    }


def update_link_permission(cursor: Cursor, link_permission_id: str, permissions: int) -> dict[str, Any]:
    cursor.execute('''
        UPDATE LinkPermission
        SET permissions = ?
        WHERE link_permission_id = ?
        RETURNING *
    ''', (permissions, link_permission_id,))

    link_permission = cursor.fetchone()

    return {
        "link_permission_id": link_permission[0],
        "permissions": link_permission[1]
    }


def delete_link_permission(cursor: Cursor, link_permission_id: str) -> None:
    cursor.execute('''
    DELETE FROM LinkPermission
    WHERE link_permission_id = ?
    ''', (link_permission_id,))


def create_user_permission(cursor: Cursor, user_account_id: str, wishlist_id: str, permissions: int) -> dict[str, Any]:
    cursor.execute('''
        INSERT INTO UserPermission (user_account_id, wishlist_id, permissions)
        VALUES (?, ?, ?)
        RETURNING *
    ''', (user_account_id, wishlist_id, permissions))
    new_user_permission = cursor.fetchone()

    return dict(
        zip([
            "user_account_id",
            "wishlist_id",
            "permissions"
        ],
            new_user_permission)
    )


def delete_user_permission(cursor: Cursor, user_account_id: str, wishlist_id: str) -> None:
    cursor.execute('''
        DELETE FROM UserPermission
        WHERE user_account_id = ?
        AND wishlist_id = ?
    ''', (user_account_id, wishlist_id))


def update_user_permission(cursor: Cursor, user_account_id: str, wishlist_id: str, permissions: int) -> dict[str, Any]:
    cursor.execute('''
        UPDATE UserPermission
        SET permissions = ?
        WHERE user_account_id = ?
        AND wishlist_id = ?
        RETURNING *
    ''', (permissions, user_account_id, wishlist_id))
    updated_user_permission = cursor.fetchone()

    return dict(
        zip([
            "user_account_id",
            "wishlist_id",
            "permissions"
        ],
            updated_user_permission)
    )


def verify_user_has_permission(cursor, wishlist_id, requester_id, permission_check_util):
    """Check if the requester has the permission to perform the action.
    @param cursor: The database cursor
    @param wishlist_id: The id of the wishlist
    @param requester_id: The id of the requester
    @param permission_check_util: permission function in api_utils that checks if the requester has the specified permission
    @return: True if the requester has the permission, False otherwise
    """
    cursor.execute('''
        SELECT permissions
        FROM UserPermission
        WHERE user_account_id = ?
        AND wishlist_id = ?
    ''', (requester_id, wishlist_id))
    requester_permission = cursor.fetchone()
    if requester_permission is None:
        return False
    requester_permission = requester_permission[0]
    has_permission = permission_check_util(requester_permission)
    return has_permission


def generate_rank(cursor: Cursor, wishlist_id: str) -> int:
    cursor.execute('''
        SELECT MAX(rank)
        FROM Item
        WHERE wishlist_id = ?
    ''', (wishlist_id,))
    max_rank = cursor.fetchone()[0]
    if max_rank is None:
        return 0
    return max_rank + 100


def create_item_in_wishlist(cursor: Cursor, item_id: str, name: str, description: str, link: str, status: int,
                            wishlist_id: str) -> dict[str, Any]:
    # Generate a rank for the new item
    rank = generate_rank(cursor, wishlist_id)
    # Create the new Item
    cursor.execute('''
        INSERT INTO Item (item_id, name, description, link, status, rank, wishlist_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING *
    ''', (item_id, name, description, link, status, rank, wishlist_id))
    new_item = cursor.fetchone()

    return dict(
        zip([
            "item_id",
            "name",
            "description",
            "image",
            "link",
            "status",
            "rank",
            "wishlist_id"
        ],
            new_item)
    )


def verify_item_exists(cursor: Cursor, item_id: str) -> bool:
    cursor.execute('''
        SELECT item_id
        FROM Item
        WHERE item_id = ?
    ''', (item_id,))
    return cursor.fetchone() is not None


def update_item(cursor, item_id, name, description, link, status):
    cursor.execute('''
        UPDATE Item
        SET name = ?, description = ?, link = ?, status = ?
        WHERE item_id = ?
        RETURNING *
    ''', (name, description, link, status, item_id))
    updated_item = cursor.fetchone()

    return dict(
        zip([
            "item_id",
            "name",
            "description",
            "image",
            "link",
            "status",
            "rank",
            "wishlist_id"
        ],
            updated_item)
    )


def get_wishlist_id_from_item(cursor, item_id):
    cursor.execute('''
        SELECT wishlist_id
        FROM Item
        WHERE item_id = ?
    ''', (item_id,))
    return cursor.fetchone()[0]


def delete_item(cursor, item_id):
    cursor.execute('''
        DELETE FROM Item
        WHERE item_id = ?
    ''', (item_id,))


def is_requester_logged_in(request):
    requester_id = request.cookies.get('user_account_id')
    is_logged_in = requester_id is not None and requester_id != ""
    return is_logged_in


def verify_link_permission_exists_with_wishlist_id(cursor, link_permission_id, wishlist_id) -> bool:
    cursor.execute('''
        SELECT 0
        FROM LinkPermission
        WHERE link_permission_id = ?
        AND wishlist_id = ?
    ''', (link_permission_id, wishlist_id,))
    return cursor.fetchone() is not None


def get_user_permission_level(cursor, user_account_id, wishlist_id):
    cursor.execute('''
        SELECT permissions
        FROM UserPermission
        WHERE user_account_id = ? AND wishlist_id = ?
    ''', (user_account_id, wishlist_id,))

    user_permission = cursor.fetchone()

    if user_permission:
        # Extract the permissions value from the query result
        permissions = user_permission[0]

        return permissions
    else:
        # Return 0 if no permissions are found
        return 0


def get_link_permission_level(cursor, link_permission_id, wishlist_id):
    cursor.execute('''
        SELECT permissions
        FROM LinkPermission
        WHERE link_permission_id = ? AND wishlist_id = ?
    ''', (link_permission_id, wishlist_id,))

    link_permission = cursor.fetchone()

    if link_permission:
        # Extract the permissions value from the query result
        permissions = link_permission[0]

        return permissions
    else:
        # Return 0 if no permissions are found
        return 0


def verify_owner_and_check_existing_name(cursor, wishlist_id, name):
    cursor.execute('''
        SELECT user_account_id
        FROM Wishlist
        WHERE wishlist_id = ? 
    ''', (wishlist_id,))

    user_account_id = cursor.fetchone()

    cursor.execute('''
        SELECT 0
        FROM Wishlist
        WHERE user_account_id = ? AND name = ?        
    ''', (user_account_id[0], name,))

    return cursor.fetchone() is not None


def get_item(cursor: Cursor, item_id: str) -> dict[str, Any]:
    cursor.execute('''
        SELECT *
        FROM Item
        WHERE item_id = ?
    ''', (item_id,))
    item = cursor.fetchone()
    return dict(
        zip([
            "item_id",
            "name",
            "description",
            "image",
            "link",
            "status",
            "rank",
            "wishlist_id"
        ],
            item)
    )


def get_wishlist_items(cursor: Cursor, wishlist_id: str) -> list[dict[Any, Any]]:
    cursor.execute('''
        SELECT *
        FROM Item
        WHERE wishlist_id = ?
    ''', (wishlist_id,))
    items = cursor.fetchall()
    return [dict(
        zip([
            "item_id",
            "name",
            "description",
            "image",
            "link",
            "status",
            "rank",
            "wishlist_id"
        ],
            item)
    ) for item in items]


def verify_link_permission_has_permission(cursor: Cursor, link_id: str, permission_check_util: callable) -> bool:
    """
    Check if the link has the permission to perform the action.
    :param cursor:
    :param link_id:
    :param permission_check_util:
    :return:
    """
    cursor.execute('''
        SELECT permissions
        FROM LinkPermission
        WHERE link_permission_id = ?
    ''', (link_id,))
    permission = cursor.fetchone()
    if permission is None:
        return False
    else:
        permission = permission[0]
        has_permission = permission_check_util(permission)
        return has_permission


def verify_comment_exists(cursor, comment_id):
    cursor.execute('''
        SELECT comment_id
        FROM Comment
        WHERE comment_id = ?
    ''', (comment_id,))
    return cursor.fetchone() is not None
