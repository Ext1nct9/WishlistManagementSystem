from endpoints.Account import add_routes as add_Account_routes
from endpoints.Login import add_routes as add_Login_routes 
from endpoints.UserPermission import add_routes as add_UserPermission_routes
from endpoints.LinkPermission import add_routes as add_LinkPermission_routes
from endpoints.Item import add_routes as add_Item_routes
from endpoints.ItemTag import add_routes as add_ItemTag_routes
from endpoints.Wishlist import add_routes as add_Wishlist_routes
from endpoints.WishlistTag import add_routes as add_WishlistTag_routes
from endpoints.Comment import add_routes as add_Comment_routes
from flask import Flask, make_response
from flask_restful import Api
from utils.api_utils import BASE_HOST, BASE_PORT


# Initialize flask
app = Flask(__name__)
api = Api(app)

# Testing routes
@app.route("/test")
def test():
    resp = make_response("test login")
    resp.set_cookie('user_account_id', '0', max_age=3600, path='/', httponly=True)
    return resp

@app.route("/end")
def end():
    resp = make_response("test logout")
    resp.set_cookie("user_account_id", expires=0)
    return resp


# Add routes
add_Account_routes(api)
add_Login_routes(api)
add_UserPermission_routes(api)
add_LinkPermission_routes(api)
add_Item_routes(api)
add_ItemTag_routes(api)
add_Wishlist_routes(api)
add_Comment_routes(api)
add_WishlistTag_routes(api)


if __name__ == "__main__":
    app.run(host=BASE_HOST, port=BASE_PORT, debug=True)
