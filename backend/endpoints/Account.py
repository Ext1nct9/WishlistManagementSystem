from flask import request
from flask_restful import Resource

# noinspection PyUnresolvedReferences
from utils import db_utils, api_utils


# add routes
def add_routes(api):
    api.add_resource(CreateAccount, '/create_account')
    api.add_resource(UpdateAccount, '/update_account')
    api.add_resource(DeleteAccount, '/delete_account')


class CreateAccount(Resource):
    # noinspection PyMethodMayBeStatic
    def put(self):
        """
        Handle PUT request to create a new user account
        """
        
        # Extract data from the JSON request body
        data = request.json
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        # Hash the password
        hashed_password = api_utils.hash_password(password)
        
        # Generate a unique user ID
        user_id = api_utils.generate_id()
        
        # Check for missing required fields in the request body
        if not email or not username or not password:
            return {'error_msg': 'Missing required fields'}, 400
        
        # Check for whitespace in the password
        if ' ' in password:
            return {'error_msg': 'Password entry must not contain whitespace'}, 400

        # Check if the password meets length and complexity requirements
        if len(password) < 10 or not any(char.isdigit() for char in password):
            return {'error_msg': 'Password must be at least 10 characters long and contain at least one number'}, 400
        
        # Create a cursor for database operations
        conn, cursor = db_utils.conn()

        # Check if the email is already in use
        cursor.execute("SELECT * FROM UserAccount WHERE email = ?", (email,))
        if cursor.fetchone():
            db_utils.close(conn, cursor)
            return {'error_msg': 'Email already in use'}, 409

        try:
            # Insert the new user account into the database
            cursor.execute('''
                INSERT INTO UserAccount (user_account_id, email, username, password)
                    VALUES (?, ?, ?, ?)
                    RETURNING *
            ''', (user_id, email, username, hashed_password))

            # Fetch the newly created user account from the database
            new_user_account = cursor.fetchone()

            db_utils.close(conn, cursor, True)
            # Return user account on success
            return {
                "user_account_id": new_user_account[0],
                "email": new_user_account[1],
                "username": new_user_account[2],
            }, 201
        except Exception as e:
            db_utils.close(conn, cursor)
            # Return error message if account creation fails
            return {""}, 500


class UpdateAccount(Resource):
    """
    Handle PUT request to update an account
    """
    @api_utils.login_required("You must be logged in to update your account.")
    def put(self):
        # Extract data from the JSON request body
        data = request.json
        user_account_id = data.get('user_account_id')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Get the user's id
        user_id = request.cookies.get('user_account_id')

        # If this is not the same user, stop
        if user_account_id != user_id:
            return {'error_msg': 'You are not authorized to update this account'}, 403

        # Connect to the database
        conn, cursor = db_utils.conn()

        # If the email is empty
        if email is None or not trim_string(email):
            return {'error_msg': 'Email entry must not be empty (no whitespace)'}, 400

        # If the username is empty 
        if username is None or not trim_string(username):
            return {'error_msg': 'Username entry must not be empty (no whitespace)'}, 400

        # If the password is empty 
        if password is None or not trim_string(password):
            return {'error_msg': 'Password entry must not be empty (no whitespace)'}, 400

        # If password does not contain at least 10 characters without whitespace
        if len(trim_string(password)) < 10:
            return {'error_msg': 'Password entry must be at least 10 characters (no whitespace) long'}, 400

        # If the password has whitespace
        if has_whitespace(password):
            return {'error_msg': 'Password entry must not contain whitespace'}, 400

        # If password does not contain at least one number
        if not has_number(password):
            return {'error_msg': 'Password entry must contain at least one number'}, 400

        # Hash the password using SHA-256
        hashed_password = api_utils.hash_password(password)

        # Update the account
        cursor.execute('''
            UPDATE UserAccount
            SET email = ?, username = ?, password = ?
            WHERE user_account_id = ?
            RETURNING * 
        ''', (email, username, hashed_password, user_id,))   

        updated_account = cursor.fetchone()

        db_utils.close(conn, cursor, True)

        return {            
            "user_account_id": updated_account[0],
            "email": updated_account[1],
            "username": updated_account[2],
        }, 200


class DeleteAccount(Resource):
    """
    Handle DELETE request to delete an account
    """
    @api_utils.login_required("You must be logged in to delete your account.")
    def delete(self):
        # Extract data from the JSON request body
        data = request.json
        user_account_id = data.get('user_account_id')

        # Get the user's id
        user_id = request.cookies.get('user_account_id')

        # If this is not the same user, stop
        if user_account_id != user_id:
            return {'error_msg': 'You are not authorized to delete this account'}, 403

        # Connect to the database
        conn, cursor = db_utils.conn()

        # Delete the account
        
        # Delete UserPermission associated to UserAccount
        cursor.execute('''
            DELETE FROM UserPermission
            WHERE user_account_id = ?
        ''', (user_id,))

        # Delete UserPermission associated to Whishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM UserPermission
            WHERE wishlist_id 
                IN (SELECT wishlist_id
                    FROM Wishlist
                    WHERE user_account_id = ?
                    )
        ''', (user_id,))

        # Delete LinkPermission associated to Whishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM LinkPermission
            WHERE wishlist_id 
                IN (SELECT wishlist_id
                    FROM Wishlist
                    WHERE user_account_id = ?
                    )
        ''', (user_id,))

        # Delete ItemTag associated to Tag associated to Whishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM ItemTag
            WHERE tag_id 
                IN (SELECT tag_id
                    FROM Tag
                    WHERE wishlist_id
                        IN (SELECT wishlist_id
                            FROM Wishlist
                            WHERE user_account_id = ?
                            )
                    )
        ''', (user_id,))

        # Delete ItemTag associated to Item associated to Whishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM ItemTag
            WHERE item_id 
                IN (SELECT item_id
                    FROM Item
                    WHERE wishlist_id
                        IN (SELECT wishlist_id
                            FROM Wishlist
                            WHERE user_account_id = ?
                            )
                    )
        ''', (user_id,))

        # Delete Comment associated to Item associated to Whishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM Comment
            WHERE item_id 
                IN (SELECT item_id
                    FROM Item
                    WHERE wishlist_id
                        IN (SELECT wishlist_id
                            FROM Wishlist
                            WHERE user_account_id = ?
                            )
                    )
        ''', (user_id,))

        # Delete Item associated to Whishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM Item
            WHERE wishlist_id 
                IN (SELECT wishlist_id
                    FROM Wishlist
                    WHERE user_account_id = ?
                    )
        ''', (user_id,))

        # Delete Tag associated to Whishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM Tag
            WHERE wishlist_id 
                IN (SELECT wishlist_id
                    FROM Wishlist
                    WHERE user_account_id = ?
                    )
        ''', (user_id,))

        # Delete Wishlist associated to UserAccount
        cursor.execute('''
            DELETE FROM Wishlist
            WHERE user_account_id = ?
        ''', (user_id,))

        # Delete UserAccount
        cursor.execute('''
            DELETE FROM UserAccount
            WHERE user_account_id = ?
        ''', (user_id,)) 

        db_utils.close(conn, cursor, True)

        return {}, 204


def has_whitespace(password):
    for c in password:
        if c == ' ' or c == '\t':
            return True
    return False


def trim_string(password):
    return password.replace(" ", "").replace("\t", "")


def has_number(password):
    for c in password:
        if c.isdigit():
            return True
    return False
