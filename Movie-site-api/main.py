import json
from flask import Flask, request, jsonify
import sqlite3
import datetime
from flask_cors import CORS
from flask_restful import Resource, Api, marshal_with, fields
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
import jwt
import string
import random
import time
import math

app = Flask(__name__)
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

user_fields = {
    'id': fields.Integer,
    'public_id': fields.String,
    'username': fields.String,
    'password': fields.String
}

class MovieModel(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)

movie_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'year': fields.Integer
}

def token_required(f):
    """Decorator yo check token
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        global user
        token = None
        current_user = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = UserModel.query.filter_by(public_id=data['public_id']).first()
            user = current_user
        except:
            return 401
        return f(current_user, *args, **kwargs)
    return decorator

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@marshal_with(user_fields)
@token_required
def get(self, current_user):
    result = UserModel.query.all()

    return result

@app.route('/v1/register', methods=['POST'])
def register():
    """register user
    """
    args = request.get_json(force=True)
    data = UserModel(
        public_id=id_generator(80),
        username=args['username'],
        password=args['password'],
    )
    db.session.add(data)
    db.session.commit()
    return "succes", 200

@token_required
def delete():
    input_json = request.get_json(force=True)
    id = input_json['id']
    result = UserModel.query.filter_by(id=id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        return "succes", 200
    return "User not found", 404

@token_required
def put(self, current_user):
    input_json = request.get_json(force=True)
    id = input_json['id']
    username = input_json['username']
    password=input_json['password']

    result = UserModel.query.filter_by(id=id).first()

    if result:
        result.username = username
        result.password = password
        db.session.commit()
        return "succes", 200
        
    return "User not found", 404

@app.route('/v1/login', methods=['POST'])
def login():
    input_json = request.get_json(force=True)
    username = input_json['username']
    password = input_json['password']
    user = UserModel.query.filter(UserModel.username==username).first()

    if user:
        if password == user.password:
            token = jwt.encode({'public_id': user.public_id}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token, 'user': user.username})
        return "unauthorized", 401
    
    return "unauthorized", 401

@app.route('/v1/checklogin')
def check_login():
    headers = request.headers
    token = headers['token']
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return "succes", 200
    except:
        return "unauthorized", 401

@marshal_with(movie_fields)
@app.route('/v1/movies', methods=['GET'])
def get_movies():
    """Get movies from API
    """
    page = int(request.args.get('page'))
    result = MovieModel.query.paginate(page=page, per_page=10, error_out=True)

    return result.items, 200
    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(host='192.168.178.69',port=1500, debug=True, threaded=True)