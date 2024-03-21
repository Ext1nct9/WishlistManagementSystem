from flask import request
from functools import wraps
import hashlib
import os
import uuid

BASE_HOST = "0.0.0.0"

BASE_PORT = 8000

BASE_URL = f"http://{'localhost' if BASE_HOST == '0.0.0.0' else BASE_HOST}:{BASE_PORT}"


# Decorator for endpoints that need to check that the requester is logged in
'''
example:
    from . import api_utils
    class MyResource(Resource):
        @api_utils.login_required("You must be logged in to get the list of MyResources.")
        def get():
            ...

Before processing the GET request, api_utils will check if the requester is logged in
(i.e. if the cookie "user_account_id" is set).
If yes, then the code inside `get()` will run.
If no, the code inside `get()` will not run and the request will get a response containing
the error message specified in <error_msg> and a return code of 401 Unauthorized.
'''


def login_required(error_msg: str = "Login required."):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not request.cookies.get("user_account_id"):
                return {"error_msg": error_msg}, 401
            return func(*args, **kwargs)

        return decorated_function

    return decorator


# Generate a random ID
def generate_id() -> str:
    return str(uuid.uuid4())


# Hash and salt a password
def hash_password(password: str, salt: bytes = None) -> str:
    """
    Hash and salt a given password
    @param password: the password to salt and hash
    @param salt: the salt to use (default = None generates a random salt)
    @return str: format = "<salt>:<hashed_password>\"
    """
    if salt is None:
        # Generate random salt
        salt = os.urandom(32)

    # Combine the password and salt
    salted_password = password.encode() + salt

    # Create a hash using SHA-256
    hashed_password = hashlib.sha256(salted_password).hexdigest()

    # Concatenate salt and hash with a delimiter
    salt_and_hash = salt.hex() + ":" + hashed_password

    return salt_and_hash


# Verify a password
def verify_password(cursor, user_account_id: int, password: str) -> bool:
    """
    Verify if a given password matches the hash in the DB
    @param cursor: cursor to the DB
    @param user_account_id: id of the UserAccount's password to match
    @param password: password to hash and match
    @return bool: True if the password matches the hash, False otherwise
    @throws sqlite3.Error: if there is an error accessing the DB
    """
    # Get hash from DB
    cursor.execute('''
        SELECT password
        FROM UserAccount
        WHERE user_account_id = ?
    ''', (user_account_id,))
    expected = cursor.fetchone()[0]

    # Return False if UserAccount not found
    if expected is None:
        return False

    # Split the salt and the hash
    salt_hex, _ = expected.split(':')

    # Get the hash with the proper salt
    attempt = hash_password(password, bytes.fromhex(salt_hex))

    # Compare the attempt to the expected hash and return the result
    return attempt == expected


'''
Permissions:
    ~LSB~
    view wishlist
    edit wishlist
    edit items
    edit tags
    set tags
    comment
    ~MSB~
'''


# Check if a permissions integer can: view wishlist
def can_view(permissions: int) -> bool:
    return bool(permissions & 0b00000001)


# Check if a permissions integer can: edit wishlist
def can_edit_wishlist(permissions: int) -> bool:
    return bool(permissions & 0b00000010)


# Check if a permissions integer can: edit items
def can_edit_items(permissions: int) -> bool:
    return bool(permissions & 0b00000100)


# Check if a permissions integer can: edit tags
def can_edit_tags(permissions: int) -> bool:
    return bool(permissions & 0b00001000)


# Check if a permissions integer can: set tags
def can_set_tags(permissions: int) -> bool:
    return bool(permissions & 0b00010000)


# Check if a permissions integer can: comment
def can_comment(permissions: int) -> bool:
    return bool(permissions & 0b00100000)
