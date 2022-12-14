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
from fields import *

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

class MovieModel(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), unique=True, nullable=False)

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

# Users =================================================================================================

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/v1/users', methods=['GET'])
@marshal_with(user_fields)
def get_users():
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

@app.route('/v1/users', methods=['POST'])
def add_user():
    input_json = request.get_json(force=True)
    username = input_json['username']
    password = input_json['password']
    data = UserModel(
        public_id=id_generator(80),
        username=username,
        password=password,
    )
    db.session.add(data)
    db.session.commit()
    return "succes", 200

@app.route('/v1/users', methods=['DELETE'])
def delete_user():
    input_json = request.get_json(force=True)
    id = input_json['id']
    result = UserModel.query.filter_by(id=id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        return "succes", 200
    return "User not found", 404

@app.route('/v1/users', methods=['PUT'])
def edit_user():
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

@app.route('/v1/checklogin', methods=['POST'])
def check_login():
    headers = request.headers
    token = headers['token']
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return "succes", 200
    except:
        return "unauthorized", 401

# Movies =================================================================================================

@app.route('/v1/movies', methods=['GET'])
@marshal_with(movie_fields)
def get_movies():
    """Get movies from API
    """
    page = int(request.args.get('page'))
    result = MovieModel.query.paginate(page=page, per_page=10, error_out=True)

    return result.items, 200

@app.route('/v1/movies', methods=['PUT'])
def put_movies():
    """Put movies from API
    """
    input_json = request.get_json(force=True)
    id = input_json['id']
    title = input_json['title']
    description = input_json['description']
    year = input_json['year']
    image = input_json['image']

    result = MovieModel.query.filter_by(id=id).first()

    if result:
        result.title = title
        result.description = description
        result.year = year
        result.image = image
        db.session.commit()
        return "succes", 200

    return "id not found", 404

@app.route('/v1/movies', methods=['POST'])
def post_movies():
    """Post movies from API
    """
    input_json = request.get_json(force=True)
    title = input_json['title']
    description = input_json['description']
    year = input_json['year']
    image = input_json['image']

    data = MovieModel(
        title=title,
        description=description,
        year=year,
        image=image
    )
    #TODO some more edge case checks?
    db.session.add(data)
    db.session.commit()
    return "succes", 200
    
@app.route('/v1/movies', methods=['DELETE'])
def delete_movies():
    """Delete movies from API
    """
    input_json = request.get_json(force=True)
    id = input_json['id']
    result = MovieModel.query.filter_by(id=id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        return "succes", 200
    return "id not found", 404

if __name__ == "__main__":
    app.run(host='192.168.178.69',port=1500, debug=True, threaded=True)