from flask_restful import fields

movie_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'year': fields.Integer,
    'image': fields.String
}

user_fields = {
    'id': fields.Integer,
    'public_id': fields.String,
    'username': fields.String,
    'password': fields.String
}
