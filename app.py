"""
This is a starting point for the backend of furrily app, you may wanna
import the controllers here and add the resources
"""

from datetime import timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity


from models import user
from controllers import auth, user as userController, gigs as gigsController
from constants import SECRET_KEY
import connector

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours = 24)

app.register_blueprint(auth.auth)
app.register_blueprint(userController.users)
app.register_blueprint(gigsController.gigs)

jwt = JWT(app, user.User.authenticate, user.User.identity)

@app.route('/')
def test():
    """
        Use this api to test if server is running or not
    """
    return jsonify({"response" : "server is up and running"})

if __name__ == '__main__':
    app.run(debug=True)
