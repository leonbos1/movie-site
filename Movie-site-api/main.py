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
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String
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


class User(Resource):
    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @marshal_with(user_fields)
    @token_required
    def get(self, current_user):
        result = UserModel.query.all()

        return result

    def post(self):
        """register user
        """
        args = request.get_json(force=True)
        data = UserModel(
            public_id=self.id_generator(80),
            username=args['username'],
            password=args['password'],
        )
        db.session.add(data)
        db.session.commit()
        return 200

    @token_required
    def delete(self, current_user):
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

class Login(Resource):
    def post(self):
       # try:
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

        #except:
         #   return "unauthorized", 401

@app.route('/checklogin')
def check_login():
    headers = request.headers
    token = headers['token']
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return "succes", 200
    except:
        return "unauthorized", 401

api.add_resource(Login, "/login")
api.add_resource(User, "/user")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='192.168.178.69',port=1500, debug=True, threaded=True)