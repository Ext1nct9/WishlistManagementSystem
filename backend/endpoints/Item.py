from flask import request
from flask_restful import Resource
import json

# noinspection PyUnresolvedReferences
from utils import api_utils, db_utils

# noinspection PyUnresolvedReferences
from utils.db_procedures import (
    create_item_in_wishlist,
    delete_item,
    is_requester_using_link,
    is_requester_logged_in,
    get_item,
    get_wishlist_id_from_item,
    get_wishlist_items,
    update_item,
    verify_item_exists,
    verify_link_permission_exists,
    verify_link_permission_has_permission,
    verify_requester_is_owner_of_wishlist,
    verify_user_has_permission,
    verify_wishlist_exists
)


def add_routes(api):
    api.add_resource(CreateItem, '/create_item/<string:wishlist_id>')
    api.add_resource(UpdateItem, '/update_item/<string:item_id>')
    api.add_resource(DeleteItem, '/delete_item/<string:item_id>')
    api.add_resource(ViewItem, '/view_item/<string:item_id>')
    api.add_resource(ViewWishlistItems, '/view_wishlist_items/<string:wishlist_id>')


class CreateItem(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self, wishlist_id=None):
        """
        Create a new item in a wishlist - API request
        :param wishlist_id: The id of the wishlist to create the item in
        """

        # Parse data
        data = json.loads(request.data)

        # Generate a new item_id
        item_id = api_utils.generate_id()

        # Get the parameters
        name = data.get('name')
        description = data.get('description')
        link = data.get('link')
        status = data.get('status')

        using_link = is_requester_using_link(request)
        logged_in = is_requester_logged_in(request)

        # Validate the parameters
        if name is None:
            return {"error_msg": "<name> cannot be blank."}, 400
        if wishlist_id is None:
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target Wishlist exists
        if not verify_wishlist_exists(cursor, wishlist_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Wishlist does not exist."}, 400

        check_user_permission = False
        check_link_permission = False

        if using_link:
            link_id = request.args.get('link_permission_id')
            # Verify link permission exists
            if not verify_link_permission_exists(cursor, link_id):
                db_utils.close(conn, cursor)
                return {"error_msg": "The target Link does not exist."}, 400
            check_link_permission = verify_link_permission_has_permission(cursor, link_id, api_utils.can_edit_items)
            if not logged_in and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "Your link does not have permission to create an Item."}, 403

        if logged_in:
            print("Requester is logged in")
            requester_id = request.cookies.get("user_account_id")

            owner_of_wishlist = verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id)
            has_permission = verify_user_has_permission(cursor, wishlist_id, requester_id, api_utils.can_edit_items)

            check_user_permission = owner_of_wishlist or has_permission

            if not check_user_permission and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "You do not have permission to create an Item."}, 403

        if check_user_permission or check_link_permission:
            # Create the new Item
            new_item = create_item_in_wishlist(cursor, item_id, name, description, link, status, wishlist_id)
            db_utils.close(conn, cursor, True)
            # Return the new Item
            return new_item, 201

        else:
            db_utils.close(conn, cursor)
            return {"error_msg": "You must be logged in to create an Item."}, 403


class UpdateItem(Resource):
    # noinspection PyMethodMayBeStatic
    def put(self, item_id=None):
        """
        Update an item in a wishlist - API request
        :param item_id: The id of the item to update
        """

        # Parse data
        data = json.loads(request.data)

        # Get the parameters
        name = data.get('name')
        description = data.get('description')
        link = data.get('link')
        status = data.get('status')

        using_link = is_requester_using_link(request)
        logged_in = is_requester_logged_in(request)

        # Validate the parameters
        if name is None:
            return {"error_msg": "<name> cannot be blank."}, 400
        if item_id is None:
            return {"error_msg": "<item_id> cannot be blank."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target Item exists
        if not verify_item_exists(cursor, item_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Item does not exist."}, 400

        # Get the wishlist_id
        wishlist_id = get_wishlist_id_from_item(cursor, item_id)

        check_user_permission = False
        check_link_permission = False

        if using_link:
            link_id = request.args.get('link_permission_id')
            # Verify link permission exists
            if not verify_link_permission_exists(cursor, link_id):
                db_utils.close(conn, cursor)
                return {"error_msg": "The target Link does not exist."}, 400
            check_link_permission = verify_link_permission_has_permission(cursor, link_id, api_utils.can_edit_items)
            if not logged_in and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "Your link does not have permission to edit items in this wishlist"}, 403

        if logged_in:
            print("Requester is logged in")
            requester_id = request.cookies.get("user_account_id")

            owner_of_wishlist = verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id)
            has_permission = verify_user_has_permission(cursor, wishlist_id, requester_id, api_utils.can_edit_items)

            check_user_permission = owner_of_wishlist or has_permission

            if not check_user_permission and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "You do not have permission to edit items in this wishlist"}, 403

        if check_user_permission or check_link_permission:
            # Update the Item
            updated_item = update_item(cursor, item_id, name, description, link, status)
            db_utils.close(conn, cursor, True)
            # Return the updated Item
            return updated_item, 200

        else:
            db_utils.close(conn, cursor)
            return {"error_msg": "You do not have permission to edit items in this wishlist."}, 403


class DeleteItem(Resource):
    # noinspection PyMethodMayBeStatic
    def delete(self, item_id=None):
        """
        Delete an item in a wishlist - API request
        :param item_id: The id of the item to delete
        """

        # Parse data
        data = json.loads(request.data)

        using_link = is_requester_using_link(request)
        logged_in = is_requester_logged_in(request)

        # Validate the parameters
        if item_id is None:
            return {"error_msg": "<item_id> cannot be blank."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target Item exists
        if not verify_item_exists(cursor, item_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Item does not exist."}, 400

        # Get the wishlist_id
        wishlist_id = get_wishlist_id_from_item(cursor, item_id)

        check_user_permission = False
        check_link_permission = False

        if using_link:
            link_id = request.args.get('link_permission_id')
            # Verify link permission exists
            if not verify_link_permission_exists(cursor, link_id):
                db_utils.close(conn, cursor)
                return {"error_msg": "The target Link does not exist."}, 400
            check_link_permission = verify_link_permission_has_permission(cursor, link_id, api_utils.can_edit_items)
            if not logged_in and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "Your link does not have permission to delete items in this wishlist."}, 403

        if logged_in:
            print("Requester is logged in")
            requester_id = request.cookies.get("user_account_id")

            owner_of_wishlist = verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id)
            has_permission = verify_user_has_permission(cursor, wishlist_id, requester_id, api_utils.can_edit_items)

            check_user_permission = owner_of_wishlist or has_permission

            if not check_user_permission and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "You do not have permission to delete items in this wishlist."}, 403

        if check_user_permission or check_link_permission:
            delete_item(cursor, item_id)
            db_utils.close(conn, cursor, True)
            return {}, 204
        else:
            db_utils.close(conn, cursor)
            return {"error_msg": "You must be logged in to delete an Item."}, 403


class ViewItem(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, item_id=None):
        """
        View an item in a wishlist - API request
        :param item_id: The id of the item to view
        """

        # Parse data
        data = json.loads(request.data)

        using_link = is_requester_using_link(request)
        logged_in = is_requester_logged_in(request)

        # Validate the parameters
        if item_id is None:
            return {"error_msg": "<item_id> cannot be blank."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target Item exists
        if not verify_item_exists(cursor, item_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Item does not exist."}, 400

        # Get the wishlist_id
        wishlist_id = get_wishlist_id_from_item(cursor, item_id)

        check_user_permission = False
        check_link_permission = False

        if using_link:
            link_id = request.args.get('link_permission_id')
            # Verify link permission exists
            if not verify_link_permission_exists(cursor, link_id):
                db_utils.close(conn, cursor)
                return {"error_msg": "The target Link does not exist."}, 400
            check_link_permission = verify_link_permission_has_permission(cursor, link_id, api_utils.can_edit_items)
            if not logged_in and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "Your link does not have permission to view the items in this wishlist."}, 403

        if logged_in:
            print("Requester is logged in")
            requester_id = request.cookies.get("user_account_id")

            owner_of_wishlist = verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id)
            has_permission = verify_user_has_permission(cursor, wishlist_id, requester_id, api_utils.can_edit_items)

            check_user_permission = owner_of_wishlist or has_permission

            if not check_user_permission and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "You do not have permission to view the items in this wishlist."}, 403

        if check_user_permission or check_link_permission:
            item = get_item(cursor, item_id)
            db_utils.close(conn, cursor)
            return item, 200
        else:
            db_utils.close(conn, cursor)
            return {"error_msg": "You must be logged in to view an Item."}, 403


class ViewWishlistItems(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, wishlist_id=None):
        """
        View a wishlist - API request
        :param wishlist_id: The id of the wishlist to view
        """

        # Parse data
        data = json.loads(request.data)

        using_link = is_requester_using_link(request)
        logged_in = is_requester_logged_in(request)

        # Validate the parameters
        if wishlist_id is None:
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target Wishlist exists
        if not verify_wishlist_exists(cursor, wishlist_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Wishlist does not exist."}, 400

        check_user_permission = False
        check_link_permission = False

        if using_link:
            link_id = request.args.get('link_permission_id')
            # Verify link permission exists
            if not verify_link_permission_exists(cursor, link_id):
                db_utils.close(conn, cursor)
                return {"error_msg": "The target Link does not exist."}, 400
            check_link_permission = verify_link_permission_has_permission(cursor, link_id, api_utils.can_edit_items)
            if not logged_in and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "Your link does not have permission to view the items in this wishlist."}, 403

        if logged_in:
            print("Requester is logged in")
            requester_id = request.cookies.get("user_account_id")

            owner_of_wishlist = verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id)
            has_permission = verify_user_has_permission(cursor, wishlist_id, requester_id, api_utils.can_edit_items)

            check_user_permission = owner_of_wishlist or has_permission

            if not check_user_permission and not check_link_permission:
                db_utils.close(conn, cursor)
                return {"error_msg": "You do not have permission to view the items in this wishlist."}, 403

        if check_user_permission or check_link_permission:
            items = get_wishlist_items(cursor, wishlist_id)
            db_utils.close(conn, cursor)
            return items, 200
        else:
            db_utils.close(conn, cursor)
            return {"error_msg": "You must be logged in to view items in a wishlist."}, 403
