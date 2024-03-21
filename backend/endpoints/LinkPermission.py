from flask import request
from flask_restful import Resource
import json

# noinspection PyUnresolvedReferences
from utils import api_utils, db_utils, db_procedures


def add_routes(api):
    api.add_resource(
        LinkPermission,
        '/wishlist/<string:wishlist_id>/permission_link'
    )

    api.add_resource(
        LinkPermissionWithId,
        '/wishlist/<string:wishlist_id>/permission_link/<string:link_permission_id>'
    )


class LinkPermission(Resource):
    @api_utils.login_required("You must be logged in to view permission links for a wishlist.")
    def get(self, wishlist_id=None):
        """
        Get all permission links for a wishlist.
        :param wishlist_id: the id of the wishlist to get permission links for
        :return: 200 success: a list of permission links for the wishlist,
                    400 bad request: the wishlist_id is missing,
                    403 forbidden: the requester is not the owner of the wishlist,
                    404 not found: the wishlist does not exist
        """

        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        # connect to the database
        conn, cursor = db_utils.conn()

        requester_id = request.cookies.get('user_account_id')

        # Verify that the target wishlist exists and the requester is the owner of the wishlist
        if not db_procedures.verify_requester_is_owner_of_wishlist(
                cursor,
                wishlist_id,
                requester_id
        ):
            db_utils.close(conn, cursor)
            return {
                "error_msg": "The requested wishlist " +
                             str(wishlist_id) +
                             " does not exist, or you do not have access to it."
            }, 404

        # get the permission links
        permission_links = db_procedures.get_all_link_permissions_for_wishlist(cursor, wishlist_id)

        # query done, close the connection
        db_utils.close(conn, cursor)

        return permission_links, 200

    @api_utils.login_required("You must be logged in to create a permission link.")
    def post(self, wishlist_id=None):
        """
        Create a new permission link for a wishlist.
        :param wishlist_id: the id of the wishlist to create a permission link for
        :return: 201 created: the new permission link,
                    400 bad request: the wishlist_id is missing, or the permissions is missing or invalid,
                    403 forbidden: the requester is not the owner of the wishlist,
                    404 not found: the wishlist does not exist,
                    409 conflict: the permission link already exists
        """

        # Parse data
        data = json.loads(request.data)

        # Get the parameters
        permissions = data.get('permissions')

        if not isinstance(permissions, int) or permissions < 0 or permissions > 255:
            return {"error_msg": "<permissions> must be an integer between 0 and 255."}, 400

        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        # connect to the database
        conn, cursor = db_utils.conn()

        requester_id = request.cookies.get('user_account_id')

        # Verify that the target wishlist exists and the requester is the owner of the wishlist
        if not db_procedures.verify_requester_is_owner_of_wishlist(
                cursor,
                wishlist_id,
                requester_id
        ):
            db_utils.close(conn, cursor)
            return {
                "error_msg": "The requested wishlist " +
                             str(wishlist_id) +
                             " does not exist, or you do not have access to it."
            }, 404

        # Create the new LinkPermission
        link_permission = db_procedures.create_link_permission_for_wishlist(cursor, wishlist_id, permissions)

        # creation done, close the connection
        db_utils.close(conn, cursor, True)

        return link_permission, 201


class LinkPermissionWithId(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, wishlist_id=None, link_permission_id=None):
        """
        Validate a permission link for a wishlist.
        :param wishlist_id: the id of the wishlist to validate a permission link for
        :param link_permission_id: the id of the permission link to validate
        :return: 200 success: the permission link,
                    404 not found: the wishlist or permission link does not exist (i.e. invalid)
        """

        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        if link_permission_id is None or link_permission_id == "":
            return {"error_msg": "<link_permission_id> cannot be blank."}, 400

        # connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target wishlist exists
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            db_utils.close(conn, cursor)
            return {
                "error_msg": "The requested wishlist " +
                             str(wishlist_id) +
                             " does not exist."
            }, 404

        # Verify that the target LinkPermission exists
        if not db_procedures.verify_link_permission_exists(cursor, link_permission_id):
            db_utils.close(conn, cursor)
            return {
                "error_msg": "The requested permission link " +
                             str(link_permission_id) +
                             " does not exist."
            }, 404

        # get the permission link
        link_permission = db_procedures.get_link_permission(cursor, link_permission_id)

        # query done, close the connection
        db_utils.close(conn, cursor)

        return link_permission, 200

    @api_utils.login_required("You must be logged in to update a permission link.")
    def put(self, wishlist_id=None, link_permission_id=None):
        """
        Update a permission link for a wishlist.
        :param wishlist_id: the id of the wishlist to update a permission link for
        :param link_permission_id: the id of the permission link to update
        :return: 200 success: the updated permission link,
                    400 bad request: the wishlist_id or link_permission_id is missing,
                        or the permissions is missing or invalid,
                    403 forbidden: the requester is not the owner of the wishlist,
                    404 not found: the wishlist or permission link does not exist
        """

        # Parse data
        data = json.loads(request.data)

        # Get the parameters
        permissions = data.get('permissions')

        if not isinstance(permissions, int) or permissions < 0 or permissions > 255:
            return {"error_msg": "<permissions> must be an integer between 0 and 255."}, 400

        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        if link_permission_id is None or link_permission_id == "":
            return {"error_msg": "<link_permission_id> cannot be blank."}, 400

        # connect to the database
        conn, cursor = db_utils.conn()

        requester_id = request.cookies.get('user_account_id')

        # Verify that the target wishlist exists and the requester is the owner of the wishlist
        if not db_procedures.verify_requester_is_owner_of_wishlist(
                cursor,
                wishlist_id,
                requester_id
        ):
            db_utils.close(conn, cursor)
            return {
                "error_msg": "The requested wishlist " +
                             str(wishlist_id) +
                             " does not exist, or you do not have access to it."
            }, 404

        # Verify that the target LinkPermission exists
        if db_procedures.verify_link_permission_exists(cursor, link_permission_id):
            # Update the LinkPermission
            link_permission = db_procedures.update_link_permission(cursor, link_permission_id, permissions)
        else:
            # create the LinkPermission
            link_permission = db_procedures.create_link_permission_for_wishlist_with_link_permission_id(
                cursor,
                link_permission_id,
                wishlist_id,
                permissions
            )

        # update done, close the connection
        db_utils.close(conn, cursor, True)

        return link_permission, 200

    @api_utils.login_required("You must be logged in to delete a permission link.")
    def delete(self, wishlist_id=None, link_permission_id=None):
        """
        Delete a permission link for a wishlist.
        :param wishlist_id: the id of the wishlist to delete a permission link for
        :param link_permission_id: the id of the permission link to delete
        :return: 204 no content: the permission link was deleted,
                    400 bad request: the wishlist_id or link_permission_id is missing,
                    403 forbidden: the requester is not the owner of the wishlist,
                    404 not found: the wishlist or permission link does not exist
        """

        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        if link_permission_id is None or link_permission_id == "":
            return {"error_msg": "<link_permission_id> cannot be blank."}, 400

        # connect to the database
        conn, cursor = db_utils.conn()

        requester_id = request.cookies.get('user_account_id')

        # Verify that the target wishlist exists and the requester is the owner of the wishlist
        if not db_procedures.verify_requester_is_owner_of_wishlist(
                cursor,
                wishlist_id,
                requester_id
        ):
            db_utils.close(conn, cursor)
            return {
                "error_msg": "The requested wishlist " +
                             str(wishlist_id) +
                             " does not exist, or you do not have access to it."
            }, 404

        # Verify that the target LinkPermission exists
        if not db_procedures.verify_link_permission_exists(cursor, link_permission_id):
            db_utils.close(conn, cursor)
            return {
                "error_msg": "The requested permission link " +
                             str(link_permission_id) +
                             " does not exist."
            }, 404

        # Delete the LinkPermission
        db_procedures.delete_link_permission(cursor, link_permission_id)

        # deletion done, close the connection
        db_utils.close(conn, cursor, True)

        # Return a 204 response
        return {}, 204
