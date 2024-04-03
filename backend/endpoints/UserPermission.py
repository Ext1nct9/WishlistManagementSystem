from flask import request
from flask_restful import Resource
import json

# noinspection PyUnresolvedReferences
from utils import db_utils, api_utils, db_procedures


def add_routes(api):
    api.add_resource(GetUserPermissions, '/get_user_permissions/<string:wishlist_id>')
    api.add_resource(CreateUserPermission, '/create_user_permission/<string:wishlist_id>')
    api.add_resource(UserPermission, '/user_permission/<string:user_account_id>/<string:wishlist_id>')


class GetUserPermissions(Resource):

    @api_utils.login_required("You must be logged in to get UserPermissions.")
    def get(self, wishlist_id=None):
        """
        Get all UserPermissions
        :return (200): all UserPermissions
        """

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target Wishlist exists
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Wishlist does not exist."}, 400

        # Verify that the requester is the owner of the Wishlist
        requester_id = request.cookies.get('user_account_id')
        if not db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "You do not have permission to get all UserPermissions for this Wishlist."}, 403

        # Get all UserPermissions
        user_permissions = db_procedures.get_all_user_permissions_for_wishlist(cursor, wishlist_id)
        db_utils.close(conn, cursor)

        # Return the UserPermissions
        return {
            "wishlist_id": wishlist_id,
            "user_permissions": user_permissions
            }, 200


class CreateUserPermission(Resource):

    @api_utils.login_required("You must be logged in to create a UserPermission.")
    def post(self, wishlist_id=None):
        """
        Create a new user permission
        :param user_account_email: The email of the account the permission is for (in request body)
        :param wishlist_id: The id of the wishlist the permission is for
        :param permissions: The permissions for the user (in request body)
        :return (201): the new UserPermission
        """

        # Parse data
        data = json.loads(request.data)

        # Get the parameters
        user_account_email = data.get('user_account_email')
        permissions = data.get('permissions')

        # Validate the parameters
        if user_account_email is None:
            return {"error_msg": "<user_account_email> cannot be blank."}, 400
        if wishlist_id is None:
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400
        if not isinstance(permissions, int) or permissions < 0 or permissions > 255:
            return {"error_msg": "<permissions> must be an integer between 0 and 255."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target UserAccount exists
        if not db_procedures.verify_user_account_exists_by_email(cursor, user_account_email):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target UserAccount does not exist."}, 400

        # Verify that the target Wishlist exists
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Wishlist does not exist."}, 400

        # Verify that the requester is the owner of the Wishlist
        requester_id = request.cookies.get('user_account_id')
        if not db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "You do not have permission to create a UserPermission for this Wishlist."}, 403

        # Verify that the UserPermission does not already exist
        if db_procedures.verify_user_permission_exists_by_user_account_email_and_wishlist_id(cursor, user_account_email, wishlist_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "A UserPermission already exists for the target UserAccount and Wishlist."}, 400

        # Create the new UserPermission
        target_user_account = db_procedures.get_user_account_by_email(cursor, user_account_email)
        new_user_permission = db_procedures.create_user_permission(cursor, target_user_account["user_account_id"], wishlist_id, permissions)
        db_utils.close(conn, cursor, True)

        # Return the new UserPermission
        return new_user_permission, 201


class UserPermission(Resource):

    @api_utils.login_required("You must be logged in to delete a UserPermission.")
    def delete(self, user_account_id=None, wishlist_id=None):
        """
        Delete a user permission
        :param user_account_id: The id of the account the permission is for
        :param wishlist_id: The id of the wishlist the permission is for
        :return (204)
        """

        # Validate the parameters
        if user_account_id is None:
            return {"error_msg": "<user_account_id> cannot be blank."}, 400
        if wishlist_id is None:
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the requester is the owner of the Wishlist
        requester_id = request.cookies.get('user_account_id')
        if not db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "You do not have permission to delete a UserPermission for this Wishlist."}, 403

        # Verify that the UserPermission exists
        if not db_procedures.verify_user_permission_exists(cursor, user_account_id, wishlist_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target UserPermission does not exist."}, 400

        # Delete the UserPermission
        db_procedures.delete_user_permission(cursor, user_account_id, wishlist_id)
        db_utils.close(conn, cursor, True)

        # Return a 204 response
        return {}, 204

    @api_utils.login_required("You must be logged in to update a UserPermission.")
    def put(self, user_account_id=None, wishlist_id=None):
        """
        Update a user permission
        :param user_account_id: The id of the account the permission is for
        :param wishlist_id: The id of the wishlist the permission is for
        :param permissions: The new permissions
        :return (200) the updated UserPermission
        """

        # Parse data
        data = json.loads(request.data)

        # Get the parameters
        permissions = data.get('permissions')

        # Validate the parameters
        if user_account_id is None:
            return {"error_msg": "<user_account_id> cannot be blank."}, 400
        if wishlist_id is None:
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400
        if not isinstance(permissions, int) or permissions < 0 or permissions > 255:
            return {"error_msg": "<permissions> must be an integer between 0 and 255."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the requester is the owner of the Wishlist
        requester_id = request.cookies.get('user_account_id')
        if not db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, requester_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "You do not have permission to update a UserPermission for this Wishlist."}, 403

        # Verify that the UserPermission exists
        if not db_procedures.verify_user_permission_exists(cursor, user_account_id, wishlist_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target UserPermission does not exist."}, 400

        # Update the UserPermission
        updated_user_permission = db_procedures.update_user_permission(
            cursor,
            user_account_id,
            wishlist_id,
            permissions
        )

        db_utils.close(conn, cursor, True)

        # Return the updated UserPermission
        return updated_user_permission, 200
