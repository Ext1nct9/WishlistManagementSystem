from utils.api_utils import can_set_tags
from utils import db_procedures, db_utils
from flask import request
from flask_restful import Resource


def add_routes(api):
    api.add_resource(AddItemTag, '/add_tag_to_item')
    api.add_resource(RemoveItemTag, '/remove_tag_from_item')


class AddItemTag(Resource):
    '''
    Handle POST request to add a tag to an item

    @param tag_id: The id of the tag that we want to add to an item
    @param item_id: The id of the item for which we want to add a tag
    @param withlist_id: The id of the wishlist we are in
    '''
    def post(self):
        has_permission = False  # Will let us know if requester can create the ItemTag

        # Extract data from the JSON request body
        data = request.json
        item_id = data.get('item_id')
        tag_id = data.get('tag_id')
        wishlist_id = data.get('wishlist_id')

        # Connect to the database
        conn, cursor = db_utils.conn()

        # If the parameters are empty
        if not item_id:
            return {"error_msg": "An item must be selected"}, 400
        if not tag_id:
            return {"error_msg": "A tag must be selected"}, 400
        if not wishlist_id:
            return {"error_msg": "A wishlist must be selected"}, 400

        # Check if the parameters exist
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {'error_msg': 'The wishlist selected does not exist'}, 404           
        if not verify_item_exists(cursor, item_id):
            return {'error_msg': 'The item selected does not exist'}, 404           
        if not verify_tag_exists(cursor, tag_id):
            return {'error_msg': 'The tag selected does not exist'}, 404           

        # If the item already has that tag
        if verify_ItemTag_exists(cursor, item_id, tag_id):
            db_utils.close(conn, cursor)
            return {'error_msg': 'Tag is already assigned to the item'}, 409

        # If the requester is logged in
        if db_procedures.is_requester_logged_in(request):
            user_id = request.cookies.get('user_account_id')    # User is for someone who is logged in

            # If the user is an owner
            if db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_id):
                has_permission = True

            # If the user has the proper permissions
            if db_procedures.verify_user_permission_exists(cursor, user_id, wishlist_id):
                permissions = db_procedures.get_user_permission_level(cursor, user_id, wishlist_id)
                if can_set_tags(permissions):
                    has_permission = True

        # If the requester can access the wishlist via a link
        requester_link_id = request.args.get('link_permission_id')    
        if requester_link_id:
            # If the requester has the proper permissions
            if db_procedures.verify_link_permission_exists_with_wishlist_id(cursor, requester_link_id, wishlist_id):
                permissions = db_procedures.get_link_permission(cursor, requester_link_id)[1]
                if can_set_tags(permissions):
                    has_permission = True

        # If the requester has the proper permissions
        if has_permission:
            cursor.execute('''INSERT INTO ItemTag (tag_id, item_id) VALUES (?, ?) RETURNING * ''', (tag_id, item_id,))   

            item_tag = cursor.fetchone()

            db_utils.close(conn, cursor, True)

            return {
                "tag_id": item_tag[0],
                "item_id": item_tag[1],
            }, 200

        else: 
            return {'error_msg': 'Not authorized to add tags to items'}, 403

class RemoveItemTag(Resource):
    '''
    Handle DELETE request to remove a tag from an item
    
    @param tag_id: The id of the tag that we want to add to an item
    @param item_id: The id of the item for which we want to add a tag
    @param withlist_id: The id of the withlist we are in
    '''
    def delete(self):
        has_permission = False  # Will let us know if requester can delete the ItemTag

        # Extract data from the JSON request body
        data = request.json
        item_id = data.get('item_id')
        tag_id = data.get('tag_id')
        wishlist_id = data.get('wishlist_id')

        # Connect to the database
        conn, cursor = db_utils.conn()

        # If the parameters are empty
        if not item_id:
            return {"error_msg": "An item must be selected"}, 400
        if not tag_id:
            return {"error_msg": "A tag must be selected"}, 400
        if not wishlist_id:
            return {"error_msg": "A wishlist must be selected"}, 400

        # Check if the parameters exist
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {'error_msg': 'The wishlist selected does not exist'}, 404           
        if not verify_item_exists(cursor, item_id):
            return {'error_msg': 'The item selected does not exist'}, 404           
        if not verify_tag_exists(cursor, tag_id):
            return {'error_msg': 'The tag selected does not exist'}, 404    

        # If the item does not have that tag
        if not verify_ItemTag_exists(cursor, item_id, tag_id):
            db_utils.close(conn, cursor)
            return {'error_msg': 'Tag is not assigned to the item'}, 409

        # If the requester is logged in
        if db_procedures.is_requester_logged_in(request):
            user_id = request.cookies.get('user_account_id')    # User is for someone who is logged in

            # If the user is an owner
            if db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_id):
                has_permission = True

            # If the user has the proper permissions
            if db_procedures.verify_user_permission_exists(cursor, user_id, wishlist_id):
                permissions = db_procedures.get_user_permission_level(cursor, user_id, wishlist_id)
                if can_set_tags(permissions):
                    has_permission = True

        # If the requester can access the wishlist via a link
        requester_link_id = request.args.get('link_permission_id')    
        if requester_link_id:
            # If the requester has the proper permissions
            if db_procedures.verify_link_permission_exists(cursor, requester_link_id, wishlist_id):
                permissions = db_procedures.get_link_permission(cursor, requester_link_id)[1]
                if can_set_tags(permissions):
                    has_permission = True

        # If the requester has the proper permissions
        if has_permission:
            cursor.execute(f'''
                DELETE FROM ItemTag 
                WHERE tag_id = ? 
                    AND item_id = ?
            ''', (tag_id, item_id,))   

            db_utils.close(conn, cursor, True)

            return {}, 204

        else: 
            return {'error_msg': 'Not authorized to remove a tag from an item'}, 403

def verify_item_exists(cursor, item_id) -> bool:
    cursor.execute('''
                SELECT item_id
                FROM Item
                WHERE item_id = ?
            ''', (item_id,))
    return cursor.fetchone() is not None


def verify_tag_exists(cursor, tag_id) -> bool:
    cursor.execute('''
                SELECT tag_id
                FROM Tag
                WHERE tag_id = ?
            ''', (tag_id,))
    return cursor.fetchone() is not None


def verify_ItemTag_exists(cursor, item_id, tag_id):
    cursor.execute('''
        SELECT *
        FROM ItemTag
        WHERE item_id = ?
        AND tag_id = ?
    ''', (item_id, tag_id,))
    return cursor.fetchone() is not None
