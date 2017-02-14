"""
This is a starting point for the backend of furrily app, you may wanna
import the controllers here and add the resources
"""

import uuid
from datetime import timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt import JWT
import boto3

from models import user
from controllers import auth, user as userController, gigs as gigsController
from constants import SECRET_KEY
import connector

app = Flask(__name__)
CORS(app)

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

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    urls = []
    for key in request.files:
        url = upload_file(request.files[key])
        urls.append(url)
    return jsonify({"response" : urls})


def generate_file_name():
    return str(uuid.uuid4())

def get_file_extension(filename):
    return filename.split('.')[1]


def upload_file(file):
    file_ext = get_file_extension(file.filename)
    filename = generate_file_name() + '.' + file_ext
    s3 = boto3.resource('s3')
    s3.Bucket('furrily').put_object(Key=filename, Body=file.read(), ACL='public-read')
    return 'https://s3-us-west-2.amazonaws.com/furrily/' + filename


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
