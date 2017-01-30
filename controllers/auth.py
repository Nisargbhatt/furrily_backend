from flask import Blueprint, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_reqparse import RequestParser
from mongoengine import NotUniqueError

from models import user as UserModule

auth = Blueprint('auth', __name__)
jwt = JWT()

@auth.route('/api/me')
@jwt_required()
def me():
    """
        Gives basic details of current_identity
    """
    user = current_identity
    return jsonify({"response" : {
        "objectId" : user.id,
        "email" : user.email,
        "name" : user.firstname + " " + user.lastname,
        "profilePicture" : user.profilePicture,
        "profileCompleteness" : user.profileCompleteness
    }})

@auth.route('/auth/refresh')
@jwt_required()
def refresh_token():
    """
        Used to refresh_token of user
    """
    new_token = jwt.jwt_encode_callback(current_identity)
    return jsonify({"token" : new_token.decode()})

@auth.route('/api/signup', methods = ['POST'])
def signup():
    """
        Used to signup new user
    """
    parser = RequestParser()
    parser.add_argument('firstname', required=True, help='firstname is required')
    parser.add_argument('lastname', required=True, help='lastname is required')
    parser.add_argument('email', required=True, help='email is required')
    parser.add_argument('password', required=True, help='password is required')

    args = parser.parse_args()
    user = UserModule.User()
    user.firstname = args['firstname']
    user.lastname = args['lastname']
    user.email = args['email']
    user.encrypt_set_password(args['password'])
    try:
        user.save()
    except NotUniqueError:
        return jsonify({"error" : "email already exists"}), 400

    return jsonify({'jsonify' : 'success'})
