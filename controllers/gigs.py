from flask import Blueprint, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_reqparse import RequestParser

from models import user as UserModule
from models import gig as GigModule

gigs = Blueprint('gig', __name__)
jwt = JWT()

@gigs.route('/api/gigs', methods=['POST'])
@jwt_required()
def post_gig():
    user = current_identity
    parser = RequestParser()
    parser.add_argument('title', required=True, help='title is required')
    parser.add_argument('description', required=True, help='title is required')
    parser.add_argument('price', required=True, help='price is required', type=str)
    parser.add_argument('attachments', type=list)
    parser.add_argument('time', required=True, help='title is required')
    parser.add_argument('skills', required=True, help='skills', type=list)
    parser.add_argument('categories', required=True, help='categories', type=list)

    args = parser.parse_args()
    gig = GigModule.Gig()
    for argument in args:
        gig[argument] = args[argument]
    gig.postedBy = UserModule.User.objects(id=user.id).first()
    gig.save()
    return jsonify({
        'response' : 'success'
    })

@gigs.route('/api/gigs', methods=['PUT'])
@jwt_required()
def update_gig():
    user = current_identity
    parser = RequestParser()
    parser.add_argument('objectId', required=True, help='objectId is required')
    parser.add_argument('title', help='title is required')
    parser.add_argument('description', help='title is required')
    parser.add_argument('price', help='price is required', type=str)
    parser.add_argument('attachments',  type=list)
    parser.add_argument('time', help='title is required')
    parser.add_argument('skills', help='skills', type=list)
    parser.add_argument('categories', help='categories', type=list)

    args = parser.parse_args()
    gig = GigModule.Gig.objects(id=args['objectId']).first()
    for argument in args:
        if argument != objectId:
            gig[argument] = args[argument]

    gig.save()
    return jsonify({
        'response' : 'success'
    })

@gigs.route('/api/gigs/<id>', methods=['GET'])
@jwt_required()
def gigs_by_id(id):
    gigs = GigModule.Gig.objects(postedBy=id)
    responseObject = []
    for g in gigs:
        responseObject.append({
            "title" : g["title"],
            "description" : g["description"],
            "price" : g["price"],
            "attachments" : g["attachments"],
            "time" : g["time"],
            "skills" : g["skills"],
            "categories" : g["categories"]
        })
    return jsonify({"response" : responseObject})

@gigs.route('/api/review/<id>', methods=['POST'])
@jwt_required()
def review_gig(id):
    parser = RequestParser()
    parser.add_argument('feedback')
    parser.add_argument('ratings', type=int)
    args = parser.parse_args()
    ratings = UserModule.UserRatings()
    ratings.gig = GigModule.Gig.objects(id=id).first()
    ratings.client = UserModule.User.objects(id=current_identity['id']).first()
    ratings.feedback = args['feedback']
    ratings.count = args['ratings']
    ratings.save()
    return jsonify({'response' : 'ratings added'})

@gigs.route('/api/review/<id>', methods=['GET'])
def get_reviews(id):
    import pdb; pdb.set_trace()
    # my_gigs = list(map(lambda x: x.id, GigModule.Gig.objects(postedBy=id)))
    my_gigs = GigModule.Gig.objects(postedBy=id)
    ratings = UserModule.UserRatings.objects(gig__in = my_gigs)
    responseObject = []
    for r in ratings:
        responseObject.append({
               "client" : {
                    'id' : str(r.client.id),
                    'name' : r.client.firstname + " " + r.client.lastname,
               },
               "feedback" : r.feedback,
               "count" : r.count,
               "gig" : {
                   "id" : str(r.gig.id),
                   "title" : r.gig.title,
                   "description" : r.gig.description,
                   "price" : r.gig.price
               }
        })
    return jsonify({'response' : responseObject})

@gigs.route('/api/wishlist/<id>', methods=['POST'])
@jwt_required()
def add_to_wishlist(id):
    gig = GigModule.Gig.objects(id=id).first()
    user = UserModule.User.objects(id=current_identity['id']).first()
    if UserModule.UserWishList.objects(gig=gig, user=user).first():
        return jsonify({"response" : "already in wishlist"})
    wishlist = UserModule.UserWishList()
    wishlist.gig = gig
    wishlist.user = user
    wishlist.save()
    return jsonify({"response" : "added to wishlist"})

@gigs.route('/api/wishlist')
@jwt_required()
def me_wishlist():
    user = UserModule.User.objects(id=current_identity['id']).first()
    wishlist = UserModule.UserWishList.objects(user=user)
    responseObject = []
    for w in wishlist:
        responseObject.append({
            'id' : str(w.gig.id),
            'title' : w.gig.title,
            'description' : w.gig.description,
            'postedBy' : {
                'id' : str(w.gig.postedBy.id),
                'name' : str(w.gig.postedBy.firstname + " " + w.gig.postedBy.lastname),
            },
            'successRate' : w.gig.successRate
        })
    return jsonify({
        'response' : responseObject
    })

@gigs.route('/api/cart/<id>', methods=['POST'])
@jwt_required()
def add_to_cart(id):
    gig = GigModule.Gig.objects(id=id).first()
    user = UserModule.User.objects(id=current_identity['id']).first()

    if UserModule.UserCart.objects(gig=gig, user=user).first():
        return jsonify({"response" : "already in cart"})
    cart = UserModule.UserCart()
    cart.gig = gig
    cart.user = user
    cart.save()
    return jsonify({"response" : "added to cart"})

@gigs.route('/api/cart')
@jwt_required()
def me_cart():
    user = UserModule.User.objects(id=current_identity['id']).first()
    cart = UserModule.UserCart.objects(user=user)
    responseObject = []
    for w in cart:
        responseObject.append({
            'id' : str(w.gig.id),
            'title' : w.gig.title,
            'description' : w.gig.description,
            'postedBy' : {
                'id' : str(w.gig.postedBy.id),
                'name' : str(w.gig.postedBy.firstname + " " + w.gig.postedBy.lastname),
            },
            'successRate' : w.gig.successRate
        })
    return jsonify({
        'response' : responseObject
    })