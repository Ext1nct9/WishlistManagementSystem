import json

from flask import request
from flask_restful import Resource

from utils import db_utils, api_utils
from utils.db_procedures import (
    verify_item_exists,
    get_wishlist_id_from_item,
    verify_requester_is_owner_of_wishlist,
    is_requester_logged_in,
    verify_user_permission_exists,
    get_user_permission_level,
    verify_link_permission_exists_with_wishlist_id,
    get_link_permission_level,
    verify_comment_exists,
    verify_requester_is_owner_of_comment
)

def add_routes(api):
    api.add_resource(CreateComment, '/comment/<string:item_id>')
    api.add_resource(DeleteComment, '/comment/<string:comment_id>')


class CreateComment(Resource):
    def post(self, item_id: str):
        '''Create a comment on an item
        @param item_id: the id of the item to comment on'''

        data = json.loads(request.data)

        body = data.get('body')

        # validate parameters
        if item_id is None:
            return {"error_msg": "item_id cannot be blank"}, 400
        elif body is None:
            return {"error_msg": "body cannot be blank"}, 400

        # connect to db
        conn, cursor = db_utils.conn()

        # Verify that the target Item exists
        if not verify_item_exists(cursor, item_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Item does not exist."}, 400

        # get wishlist_id of the item
        wishlist_id = get_wishlist_id_from_item(cursor, item_id)

        # Initialize user_permission, link_permission to 0 (no permissions)
        user_permission = 0
        link_permission = 0

        # If the requester is logged in
        if is_requester_logged_in(request):
            # Get the user's id
            user_account_id = request.cookies.get('user_account_id')

            # Check if the requester is the owner of the wishlist
            if verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_account_id):
                user_permission = 0b00111111

            # Check if there exists a UserPermission linking the requester to the wishlist
            if verify_user_permission_exists(cursor, user_account_id, wishlist_id):
                user_permission = get_user_permission_level(cursor, user_account_id, wishlist_id)

        # If link_permission_id exists in GET parameters
        link_permission_id = request.args.get('link_permission_id')

        if verify_link_permission_exists_with_wishlist_id(cursor, link_permission_id, wishlist_id):
            # Query the permissions of the given LinkPermission
            link_permission = get_link_permission_level(cursor, link_permission_id, wishlist_id)

        # Determine the combined permission level between user_permission and link_permission
        combined_permission = user_permission | link_permission
        is_user = True if user_permission != 0 else False

        # If the requester has the proper permission to comment
        if api_utils.can_comment(combined_permission):
            # Generate a new comment_id
            comment_id = api_utils.generate_id()

            new_comment = create_comment_on_item(cursor, comment_id, request.cookies.get('user_account_id'), is_user, body, item_id)
            db_utils.close(conn, cursor, True)

            # return the new Comment
            return new_comment, 201
        else:
            db_utils.close(conn, cursor)
            return {'error_msg': 'You do not have permission to comment on this item'}, 403


class DeleteComment(Resource):
    def delete(self, comment_id: str):
        '''delete a comment
        @param: the id of the comment to delete'''

        # validate parameters
        if comment_id is None:
            return {"error_msg": "comment_id cannot be blank"}, 400

        # connect to db
        conn, cursor = db_utils.conn()

        # Verify that the target Comment exists
        if not verify_comment_exists(cursor, comment_id):
            db_utils.close(conn, cursor)
            return {"error_msg": "The target Comment does not exist."}, 400

        # Check if the requester is the owner of the comment
        if is_requester_logged_in(request):
            if verify_requester_is_owner_of_comment(cursor, comment_id, request.cookies.get('user_account_id')):
                delete_comment_on_item(cursor, comment_id)
                db_utils.close(conn, cursor, True)
                #  successful deletion
                return {}, 204

        db_utils.close(conn, cursor)
        return {'error_msg': 'You do not have permission to delete this comment'}, 403


def delete_comment_on_item(cursor, comment_id):
    cursor.execute('''
        DELETE FROM Comment
        WHERE comment_id = ?
    ''', (comment_id))


def create_comment_on_item(cursor, comment_id, user_account, is_user, body, item_id):
    cursor.execute('''
        INSERT INTO Comment (comment_id, user_info, is_account, body, item_id)
        VALUES (?,?,?,?,?)
        RETURNING *
    ''', (comment_id, user_account, is_user, body, item_id))

    new_item = cursor.fetchone()

    return dict(
        zip([
            "comment_id",
            "user_info",
            "is_account",
            "body",
            "item_id",
            "creation_datetime"
        ], new_item),
    )

