from flask import request
from flask_restful import Resource
import json

# noinspection PyUnresolvedReferences
from utils import api_utils, db_utils, db_procedures


def add_routes(api):
    api.add_resource(CreateWishlist, '/wishlist/create/<string:user_account_id>')
    api.add_resource(UpdateWishlist, '/wishlist/update/<string:wishlist_id>')
    api.add_resource(DeleteWishlist, '/wishlist/delete/<string:wishlist_id>')
    api.add_resource(ViewWishlist, '/wishlist/view/<string:wishlist_id>')
    api.add_resource(ViewWishlistByUser, '/wishlist/view_by_user/<string:user_account_id>')
    

class CreateWishlist(Resource):
    @api_utils.login_required("You must be logged in to create a Wishlist.")
    def post(self, user_account_id=None):
        """
        Create a new wishlist
        :param user_account_id: The user who wants to create a wishlist
        :param name: The name of the wishlist to create
        :param description: The description of the wishlist to create
        :return 201 success: the wishlist was created successfully
                    400 bad request: the user_account_id is missing, name is none or empty
                    403 forbidden: the wishlist name cannot be duplicated within the same user_account_id,
                    404 not found: the user_account_id does not exist
        """

        if user_account_id is None or user_account_id == "":
            return {"error_msg": "<user_account_id> cannot be blank."}, 400

        # Extract data from the JSON request body
        data = json.loads(request.data)
        
        # Get the data from request body
        
        name = data.get("name")
        description = data.get("description")

        # Generate a unique wishlist_id
        wishlist_id = api_utils.generate_id()
       
        # Check for missing required fields in the request body
        if name is None or name == "":
            return {'error_msg': 'Wishlist name cannot be blank.'}, 400

        # Connect to the db
        conn, cursor = db_utils.conn()

        if db_procedures.verify_user_account_exists(cursor, user_account_id):

            requester_id = request.cookies.get('user_account_id')

            if requester_id == user_account_id:

                # Check if the same wishlist name already exists in the account
                cursor.execute('''
                    SELECT 1 FROM Wishlist 
                    WHERE name = ? AND user_account_id = ?
                    ''', (name, user_account_id,))

                existing_wishlist = cursor.fetchone()
                if existing_wishlist:      
                    db_utils.close(conn, cursor)
                    return {'error_msg': 'Wishlist name already exist in this account.'}, 403
            
                # insert the new wishlist into the database
                else:
                    cursor.execute('''
                    INSERT INTO Wishlist (wishlist_id, name, description, user_account_id)
                    VALUES (?, ?, ?, ?)
                    ''', (wishlist_id, name, description, user_account_id))
                
                    conn.commit()

                    db_utils.close(conn, cursor, True)

                    # return the created wishlist in json
                    return {
                        "wishlist_id": wishlist_id,
                        "name": name,
                        "description": description,
                        "user_account_id": user_account_id,
                    }, 201
                
            else:
                return {'error_msg': 'You do not have permission to create the wishlist'}, 403
            
        else:
            return {"error_msg": "The user_account_id does not exist."}, 404

        
class UpdateWishlist(Resource):
    # noinspection PyMethodMayBeStatic
    def put(self, wishlist_id=None):
        """
        Update a wishlist
        :param wishlist_id: The id of the wishlist to update
        :return 200 success: the wishlist was updated successfully
                    400 bad request: the wishlist name is missing,
                    403 forbidden: the requester doesn't have permission to edit,
                        or the wishlist name under then owner already exist
                    404 not found: the wishlist does not exist
        """
        
        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400
        
        # Parse data
        data = json.loads(request.data)

        # Get the parameters
        name = data.get('name')
        description = data.get('description')

        if name is None or name == "":
            return {'error_msg': 'Wishlist name cannot be blank.'}, 400

        # Initialize user_permission, link_permission to 0 (no permissions)
        user_permission = 0
        link_permission = 0

        # Create a cursor for database operations
        conn, cursor = db_utils.conn()

        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {"error_msg": "The target Wishlist does not exist."}, 404
        
        # Cehck if the name exists in the user account
        if db_procedures.verify_owner_and_check_existing_name(cursor, wishlist_id, name):
            return {'error_msg': 'Wishlist name already exist in this account.'}, 403

        # If the requester is logged in
        if db_procedures.is_requester_logged_in(request):
            # Get the user's id
            user_account_id = request.cookies.get('user_account_id')

            # Check if the requester is the owner of the wishlist
            if db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_account_id):
                user_permission = 0b00111111

            # Check if there exists a UserPermission linking the requester to the wishlist
            if db_procedures.verify_user_permission_exists(cursor,  user_account_id, wishlist_id):
                user_permission = db_procedures.get_user_permission_level(cursor, user_account_id, wishlist_id)

        # If link_permission_id exists in GET parameters
        link_permission_id = request.args.get('link_permission_id')

        if db_procedures.verify_link_permission_exists_with_wishlist_id(cursor, link_permission_id, wishlist_id):
            # Query the permissions of the given LinkPermission
            link_permission = db_procedures.get_link_permission_level(cursor, link_permission_id, wishlist_id)

        # Determine the combined permission level between user_permission and link_permission
        combined_permission = user_permission | link_permission

        # If the requester has the proper permissions
        if api_utils.can_edit_wishlist(combined_permission):
        
            cursor.execute('''
                UPDATE Wishlist
                SET name = ?, description = ?
                WHERE wishlist_id = ?
            ''', (name, description, wishlist_id))
            
            cursor.execute('''
                SELECT *
                FROM Wishlist
                WHERE wishlist_id = ?
            ''', (wishlist_id,))

            update_wishlist = cursor.fetchone()
            
            # query done, close the connection
            db_utils.close(conn, cursor, True)

            # return the updated wishlist in json
            return {
                "wishlist_id": update_wishlist[0],
                "name": update_wishlist[1],
                "description": update_wishlist[2]
            }, 200
               
        else: 
            db_utils.close(conn, cursor)
            return {'error_msg': 'You do not have permission to edit this wishlist'}, 403


class DeleteWishlist(Resource):
    @api_utils.login_required("You must be logged in to delete your wishlist.")
    def delete(self, wishlist_id=None):
        """
        Delete a wishlist
        :param wishlist_id: The id of the wishlist to delete
        :param user_account_id: The owner of the wishlist
        :return  204 no content: the wishlist  was deleted,
                    400 bad request: the wishlist_id or user_account_id is missing,
                    403 forbidden: the requester is not the owner of the wishlist,
                    404 not found: the wishlist or user_account_id does not exist
        """
    
        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400


        # connect to the database
        conn, cursor = db_utils.conn()

        user_account_id = request.cookies.get('user_account_id')

        # Verify that the target wishlist exists
        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {
                "error_msg": "The target Wishlist does not exist."
                }, 404

        # Verify that the requester is the owner of the wishlist
        if not db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_account_id):
            return {
                "error_msg": "You do not have permission to delete this Wishlist."
                }, 403
 
        # Delete the wishlist from the database
        cursor.execute('''DELETE FROM Wishlist WHERE wishlist_id = ?''', (wishlist_id,))
        
        db_utils.close(conn, cursor, True)
        
        # return success message
        return {}, 204


class ViewWishlist(Resource):
    # getting a wishlist by wishlist_id
    # noinspection PyMethodMayBeStatic
    def get(self, wishlist_id=None):
        """
        get a wishlist
        :param wishlist_id: the id of the wishlist to get the wishlist info
        :return: 200 success: a wishlist information (name, description)
                    400 bad request: the wishlist_id is missing,
                    403 forbidden: the requester doesn't have a permission to view the wishlist,
                    404 not found: the wishlist does not exist
        """

        if wishlist_id is None or wishlist_id == "":
            return {"error_msg": "<wishlist_id> cannot be blank."}, 400

        # Initialize user_permission, link_permission to 0 (no permissions)
        user_permission = 0
        link_permission = 0

        # Create a cursor for database operations
        conn, cursor = db_utils.conn()

        if not db_procedures.verify_wishlist_exists(cursor, wishlist_id):
            return {"error_msg": "The target Wishlist does not exist."}, 404
        
        # If the requester is logged in
        if db_procedures.is_requester_logged_in(request):
            # Get the user's id
            user_account_id = request.cookies.get('user_account_id')

            # Check if the requester is the owner of the wishlist
            if db_procedures.verify_requester_is_owner_of_wishlist(cursor, wishlist_id, user_account_id):
                user_permission = 0b00111111

            # Check if there exists a UserPermission linking the requester to the wishlist
            if db_procedures.verify_user_permission_exists(cursor, user_account_id, wishlist_id):
                user_permission = db_procedures.get_user_permission_level(cursor, user_account_id, wishlist_id)

        # If link_permission_id exists in GET parameters
        link_permission_id = request.args.get('link_permission_id')

        if db_procedures.verify_link_permission_exists_with_wishlist_id(cursor, link_permission_id, wishlist_id):
            # Query the permissions of the given LinkPermission
            link_permission = db_procedures.get_link_permission_level(cursor, link_permission_id, wishlist_id)
    
        # Determine the combined permission level between user_permission and link_permission
        combined_permission = user_permission | link_permission

        # If the requester has the proper permissions
        if api_utils.can_view(combined_permission):
            
            # get the wishlist information
            cursor.execute('''
                SELECT wishlist_id, name, description 
                FROM Wishlist
                WHERE wishlist_id = ?
            ''', (wishlist_id,))
            
            wishlist = cursor.fetchone()
            
            # query done, close the connection
            db_utils.close(conn, cursor, True)

            # return all of the wishlists in json
            return {
                "wishlist_id": wishlist[0],
                "name": wishlist[1],
                "description": wishlist[2]
            }, 200
                
        else: 
            db_utils.close(conn, cursor)
            return {'error_msg': 'You do not have permission to view this wishlist'}, 403


class ViewWishlistByUser(Resource):
    # getting all wishlists by user
    @api_utils.login_required("You must be logged in to view all of your wishlists.")
    def get(self, user_account_id=None):
        """
        get a wishlist
        :param user_account_id: the user_account_id to get the wishlist info
        :return: 200 success: a wishlist information (wishlist_id, name, description)
                    400 bad request: the user_account_id is missing,
                    403 forbidden: the requester is not the owner of the <user_account_id>,
        """

        if user_account_id is None or user_account_id == "":
            return {"error_msg": "<user_account_id> cannot be blank."}, 400
        
        # Create a cursor for database operations
        conn, cursor = db_utils.conn()

        if db_procedures.verify_user_account_exists(cursor, user_account_id):
    
            requester_id = request.cookies.get('user_account_id')

            if requester_id is user_account_id:
                # get the wishlist information
                cursor.execute('''
                    SELECT wishlist_id, name, description FROM Wishlist
                    WHERE user_account_id = ?
                ''', (user_account_id,))
                
                user_wishlists = cursor.fetchall()
                
                if not user_wishlists:  # Check if the list is empty
                    return {"error_msg": "The user does not have any wishlist"}, 404

                # query done, close the connection
                db_utils.close(conn, cursor, True)

                user_wishlists_json = [{
                    "wishlist_id": user_wishlist[0],
                    "name": user_wishlist[1],
                    "description": user_wishlist[2],
                } for user_wishlist in user_wishlists]

                return user_wishlists_json, 200
            
            else:
                return {'error_msg': 'You do not have permission to view the wishlists with the <user_account_id>'}, 403
            
        else:
            return {"error_msg": "The target user does not exist."}, 404
