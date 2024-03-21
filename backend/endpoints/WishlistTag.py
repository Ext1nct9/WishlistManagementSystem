from flask import request
from flask_restful import Resource
import json
import random

from utils import api_utils, db_utils, db_procedures

def add_routes(api):
    api.add_resource(CreateWishlistTag, '/wishlist/<string:wishlist_id>/create_tag')
    api.add_resource(UpdateWishlistTag, '/wishlist/<string:wishlist_id>/tags/<string:tag_id>')
    api.add_resource(DeleteWishlistTag, '/wishlist/<string:wishlist_id>/tags/<string:tag_id>')
class CreateWishlistTag(Resource):

    def put(self, wishlist_id: str):
        '''Create a new tag for a wishlist
        @param wishlist_id: The id of the wishlist
        @param label: The label of the tag
        @param color: The color of the tag
        @param tag_id: The id of the tag
        @return (201): the new tag'''

        has_permission = False

        # Parse data
        data = request.json

        # Get the parameters
        label = data.get('label')
        color = data.get('color')

        #Generate a new tag_id
        tag_id = api_utils.generate_id()

        # Check for missing required fields in the request body
        if label is None or label == "":
            return {'error_msg': 'Tag label cannot be blank.'}, 400
        if color is None or color == "":
            color = generate_random_colour()

        # Validate the parameters
        if not wishlist_id:
            return {"error_msg": "A wishlist must be selected."}, 400
        

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Verify that the target Wishlist exists
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {'error_msg': 'The selected wishlist does not exist.'}, 404  
        

        # Verify that the Tag is not already in the Wishlist
        if verify_tag_in_Wishlist_label(cursor, wishlist_id, label):
            return {'error_msg': 'Tag label already exist in this wishlist.'}, 409
    
        # If the requester is logged in
        if db_procedures.is_requester_logged_in(request):
            user_id = request.cookies.get('user_account_id')    # User is for someone who is logged in

            # If the user is an owner
            if db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_id):
                has_permission = True

            # If the user has the proper permissions
            if db_procedures.verify_user_permission_exists(cursor, user_id, wishlist_id):
                permissions = db_procedures.get_user_permission_level(cursor, user_id, wishlist_id)
                if api_utils.can_edit_tags(permissions):
                    has_permission = True

        # If the requester can access the wishlist via a link
        requester_link_id = request.args.get('link_permission_id')    
        if requester_link_id:
            # If the requester has the proper permissions
            if db_procedures.verify_link_permission_exists_with_wishlist_id(cursor, requester_link_id, wishlist_id):
                has_permission = db_procedures.verify_link_permission_has_permission(cursor, requester_link_id, api_utils.can_edit_tags)

        # Create the new WishlistTag
        if has_permission:
            cursor.execute('''
                INSERT INTO Tag (tag_id, label, color, wishlist_id)
                VALUES (?, ?, ?, ?)
                RETURNING *
            ''', (tag_id, label, color, wishlist_id))

            tag = cursor.fetchone()

            db_utils.close(conn, cursor, True)

            return {
                "tag_id": tag[0],
                "label": tag[1],
                "color": tag[2],
                "wishlist_id": tag[3]
            }, 201
        
        else:
            return {'error_msg': 'Not authorized to create tags for this wishlist.'}, 403


    
     
class DeleteWishlistTag(Resource):

    def delete(self, wishlist_id: str, tag_id: str):
        '''Delete a tag from a wishlist
        @param wishlist_id: The id of the wishlist
        @param tag_id: The id of the tag
        @return (200): the deleted tag'''

        has_permission = False

        # Validate the parameters
        if not tag_id:
            return {"error_msg": "A tag must be selected."}, 400
        if not wishlist_id:
            return {"error_msg": "A wishlist must be selected."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {'error_msg': 'The selected wishlist does not exist.'}, 404  
        

        # Verify that the Tag is not already in the Wishlist
        if not verify_tag_exists(cursor, tag_id):
            return {'error_msg': 'The selected tag does not exist.'}, 404
        
        # Verify that the Tag is in the Wishlist
        if not verify_tag_in_Wishlist(cursor, wishlist_id, tag_id):
            return {'error_msg': 'The selected tag is not in the wishlist.'}, 404
        
        # If the requester is logged in
        if db_procedures.is_requester_logged_in(request):
            user_id = request.cookies.get('user_account_id')    # User is for someone who is logged in

            # If the user is an owner
            if db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_id):
                has_permission = True

            # If the user has the proper permissions
            if db_procedures.verify_user_permission_exists(cursor, user_id, wishlist_id):
                permissions = db_procedures.get_user_permission_level(cursor, user_id, wishlist_id)
                if api_utils.can_edit_tags(permissions):
                    has_permission = True

        # If the requester can access the wishlist via a link
        requester_link_id = request.args.get('link_permission_id')    
        if requester_link_id:
            # If the requester has the proper permissions
            if db_procedures.verify_link_permission_exists_with_wishlist_id(cursor, requester_link_id, wishlist_id):
                has_permission = db_procedures.verify_link_permission_has_permission(cursor, requester_link_id, api_utils.can_edit_tags)

        # Delete the Tag from the Wishlist
        if has_permission:
            cursor.execute(''' 
                DELETE FROM Tag
                WHERE tag_id = ?
                RETURNING *
            ''', (tag_id,))

            deleted_tag = cursor.fetchone()
            db_utils.close(conn, cursor, True)
        
            # return success message
            return {}, 204
        else:
            return {'error_msg': 'Not authorized to delete tags for this wishlist.', }, 403
        
class UpdateWishlistTag(Resource):    

    def post(self, wishlist_id: str, tag_id: str):
        '''Update a tag for a wishlist
        @param wishlist_id: The id of the wishlist
        @param tag_id: The id of the tag
        @return (200): the updated tag'''

        has_permission = False

        # Validate the parameters
        if not tag_id:
            return {"error_msg": "A tag must be selected."}, 400
        if not wishlist_id:
            return {"error_msg": "A wishlist must be selected."}, 400

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Parse data
        data = request.json

        #Get the parameters
        label = data.get('label')
        color = data.get('color')

        # Check for missing required fields in the request body
        if label is None or label == "":
            return {'error_msg': 'Tag label cannot be blank.'}, 400
        if color is None or color == "":
            color = generate_random_colour()

        # Verify that the target Wishlist exists
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {"error_msg": "The selected Wishlist does not exist."}, 404
        
        # Verify that the Tag exists
        if not verify_tag_exists(cursor, tag_id):
            return {'error_msg': 'The selected tag does not exist.'}, 404
        
        # Verify that the Tag is in the Wishlist
        if not verify_tag_in_Wishlist(cursor, wishlist_id, tag_id):
            return {'error_msg': 'The selected tag is not in the wishlist.'}, 404
        
                # If the requester is logged in
        if db_procedures.is_requester_logged_in(request):
            user_id = request.cookies.get('user_account_id')    # User is for someone who is logged in

            # If the user is an owner
            if db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_id):
                has_permission = True

            # If the user has the proper permissions
            if db_procedures.verify_user_permission_exists(cursor, user_id, wishlist_id):
                permissions = db_procedures.get_user_permission_level(cursor, user_id, wishlist_id)
                if api_utils.can_edit_tags(permissions):
                    has_permission = True

        # If the requester can access the wishlist via a link
        requester_link_id = request.args.get('link_permission_id')    
        if requester_link_id:
            # If the requester has the proper permissions
            if db_procedures.verify_link_permission_exists_with_wishlist_id(cursor, requester_link_id, wishlist_id):
                has_permission = db_procedures.verify_link_permission_has_permission(cursor, requester_link_id, api_utils.can_edit_tags)


        # Update the Tag in the Wishlist
        if has_permission:
            cursor.execute('''
                UPDATE Tag
                SET label = ?, color = ?
                WHERE wishlist_id = ? AND tag_id = ?
                RETURNING *
            ''' , (label, color, wishlist_id, tag_id)) 
            updated_tag = cursor.fetchone()
            db_utils.close(conn, cursor, True)
            
            return { 
                "tag_id": updated_tag[0],
                "label":  updated_tag[1],
                "color": updated_tag[2],
                "wishlist_id": updated_tag[3]
            }, 200
        else:
            return {'error_msg': 'Not authorized to update tags for this wishlist.'}, 403
        
    


def verify_tag_exists(cursor, tag_id) -> bool:
    cursor.execute('''
                SELECT tag_id
                FROM Tag
                WHERE tag_id = ?
            ''', (tag_id,))
    return cursor.fetchone() is not None

def verify_tag_in_Wishlist(cursor, wishlist_id, tag_id) -> bool:
    cursor.execute('''
                SELECT *
                FROM Tag
                WHERE wishlist_id = ? AND tag_id = ?
            ''', (wishlist_id, tag_id))
    return cursor.fetchone() is not None

def verify_tag_in_Wishlist_label(cursor, wishlist_id, label) -> bool:
    cursor.execute('''
        SELECT *
        FROM Tag
        WHERE wishlist_id = ? AND label = ?
    ''', (wishlist_id, label))
    return cursor.fetchone() is not None


#Generate random color name
def generate_random_colour():
    color_words = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "grey", "black", "white"]
    return random.choice(color_words)

