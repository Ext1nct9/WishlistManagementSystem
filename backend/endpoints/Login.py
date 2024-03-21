from flask import request, make_response
from flask_restful import Resource

# noinspection PyUnresolvedReferences
from utils import db_utils, api_utils


def add_routes(api):
    api.add_resource(Login, '/login')


class Login(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        """
        Handle POST request to authenticate user login
        """
        
        # Extract data from the JSON request body
        data = request.json
        email = data.get('email')
        password = data.get('password')
        # Check for missing email or password in the request body
        if not email or not password:
            return {'error_msg': 'Missing email or password'}, 400
        
        # Create a cursor for database operations
        conn, cursor = db_utils.conn()

        # Check if user with given email exists in the database
        cursor.execute("SELECT * FROM UserAccount WHERE email = ?", (email,))
        user = cursor.fetchone()

        try:
            if user:
                if api_utils.verify_password(cursor, user[0], password):
                    # If passwords match, authentication successful
                    # Set a cookie containing the user_id
                    response = make_response('', 200)
                    response.set_cookie('user_account_id', str(user[0]), max_age=3600, path='/', httponly=True)
                    # return redirect(url_for('dashboard'))
                    db_utils.close(conn, cursor)
                    return response
                else:
                    # If passwords don't match, return unauthorized error
                    db_utils.close(conn, cursor)
                    return {'error_msg': 'Unauthorized: Incorrect password'}, 401
            else:
                # If user doesn't exist, return unauthorized error
                db_utils.close(conn, cursor)
                return {'error_msg': 'Unauthorized: User not found'}, 401
        except Exception as e:
            db_utils.close(conn, cursor)
            # Return error message if login fails
            return {""}, 500
