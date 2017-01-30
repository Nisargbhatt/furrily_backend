from flask import Blueprint, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_reqparse import RequestParser

from models import user as UserModule
import constants

users = Blueprint('users', __name__)
jwt = JWT()

@users.route('/api/users', methods = ['PUT'])
@jwt_required()
def edit_profile():
    user = current_identity
    parser = RequestParser()
    parser.add_argument('firstname')
    parser.add_argument('lastname')
    parser.add_argument('profilePicture')
    parser.add_argument('city')
    parser.add_argument('state')
    parser.add_argument('country')
    parser.add_argument('zipcode')
    parser.add_argument('bio')
    parser.add_argument('langauges')
    parser.add_argument('skills', type=list)
    parser.add_argument('portfolioLink', type=list)
    parser.add_argument('portfolio', type=list)

    args = parser.parse_args()
    for argument in args:
        if argument not in ['portfolioLink', 'portfolio']:
            user[argument] = args[argument]
        elif argument not in ['portfolioLink', 'portfolio']:
            user[argument] = args[argument]
        elif argument == 'portfolio':
            for portfolioObject in args[argument]:
                portfolio = UserModule.UserPortfolio()
                for p in portfolioObject:
                    portfolio[p] = portfolioObject[p]
                user.portfolio.append(portfolio)
        elif argument == 'portfolioLink':
            for portfolioLink in args['portfolioLink']:
                link = UserModule.ProfileLinks()
                for key in portfolioLink:
                    link[key] = portfolioLink[key]
                user.portfolioLinks.append(link)
    profileCompleteness = 45
    if len(user.skills) >= 3:
        profileCompleteness += 5
    if len(user.portfolioLinks) >= 2:
        profileCompleteness += 10
    if len(user.portfolio) >= 2:
        profileCompleteness += 10
    if user.address:
        profileCompleteness += 10
    if user.profilePicture != constants.PROFILE_PICTURE:
        profileCompleteness += 10

    user.profileCompleteness = profileCompleteness
    user.save()
    return jsonify({'jsonify' : 'success'})

@users.route('/api/change_password', methods=['POST'])
@jwt_required()
def change_password():
    parser = RequestParser()
    parser.add_argument('old_password', required=True, help='Old password is required')
    parser.add_argument('new_password', required=True, help='New password is required')
    args = parser.parse_args()
    user = current_identity
    user = UserModule.User.authenticate(user.email, args['old_password'])
    if not user:
        return jsonify({'response' : 'old password is invalid'})
    user.encrypt_set_password(args['new_password'])
    user.save()

    return jsonify({'response' : 'Password changed'})

@users.route('/api/users/<id>')
def getuser_byId(id):
    user = UserModule.User.objects(id=id).first()
    responseObject = {
        'firstname' : user.firstname,
        'lastname' : user.lastname,
        'email' : user.email,
        'profilePicture' : user.profilePicture,
        'country' : user.country,
        'city' : user.city,
        'state' : user.state,
        'zipcode' : user.zipcode,
        'average_ratings' : user.average_ratings,
        'langauges' : user.langauges,
        'skills' : user.skills,
        'bio' : user.bio
    }
    portfolioLinks = []
    portfolio = []

    for portfolioLink in user.portfolioLinks:
        portfolioLinks.append({
            "platform" : portfolioLink['platform'],
            "url" : portfolioLink['url']
        })
    for object in user.portfolio:
        portfolio.append({
            "title" : object['title'],
            "image" : object['image'],
            "attachments" : object['attachments'],
            "description" : object['description'],
            "skills" : object['skills']
        })

    responseObject['portfolioLinks'] = portfolioLinks
    responseObject['portfolio'] = portfolio

    return jsonify({
        "response" : responseObject
    })