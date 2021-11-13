import datetime
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND
from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
import validators
from src.database import Users, db
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")
CORS(auth)

@auth.get('/')
def welcome():
    return {"Hello":"World"}

@auth.post('/register')
def register():
    fullname=request.json['fullname']
    email=request.json['email']
    group=request.json['group']
    country=request.json['country']
    username=request.json['username']
    password=request.json['password']
    

    
    if len(fullname)<3:
        return jsonify({'error':"Not Valid"}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error':"Not Valid"}), HTTP_400_BAD_REQUEST

    if Users.query.filter_by(email=email).first() is not None:
        return jsonify({'error':f"{email} Already Exist"}), HTTP_409_CONFLICT
    
    if Users.query.filter_by(username=username).first() is not None:
        return jsonify({'error':f"{username} Already Exist"}), HTTP_409_CONFLICT

    if len(password)<4:
        return jsonify({'error':"Too short"}), HTTP_400_BAD_REQUEST


    pwd_hash = generate_password_hash(password)

    user = Users(fullname=fullname,email=email,group=group,country=country,username=username,password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "Account Created",
        'user': {
            'username': username, 'email': email
        }
    }), HTTP_201_CREATED



@auth.post('/login')
def login():
    username = request.json.get('username', '')
    password = request.json.get('password','')

    user=Users.query.filter_by(username=username).first()

    if user:
        is_pass_correct = check_password_hash(user.password,password)

        if is_pass_correct:
            expires = datetime.timedelta(days=1)
            refresh=create_refresh_token(identity=user.id)
            token=create_access_token(identity=user.id, expires_delta=expires)

            return jsonify({
                    'refresh': refresh,
                    'token': token,
                    'username': user.username,
                    'email': user.email,
                    'fullname': user.fullname,
                    'group': user.group,
                    'id': user.id,
                    'status': user.status
            }), HTTP_200_OK
    return jsonify({
        'error':"Wrong Login Details"
    }), HTTP_401_UNAUTHORIZED


@auth.get('/user')
@jwt_required()
def user():
    user_id = get_jwt_identity()
    print(user_id)

    user = Users.query.filter_by(id=user_id).first()

    return jsonify({
        'data': {
        'fullname': user.fullname,
        'email': user.email,
        'username': user.username,
        'status': user.status,
        'group': user.group,
        'id': user.id,
         }
    }), HTTP_200_OK

@auth.get('/all-unverified-users')
@jwt_required()
def get_unverified_users():
    unverified_users = Users.query.filter_by(status='unverified').order_by(Users.id.asc()).limit(10)
    
    data=[]

    for one_unverified_user in unverified_users:
        data.append({
            'id': one_unverified_user.id,
            'fullname': one_unverified_user.fullname,
            'email': one_unverified_user.email,
            'group': one_unverified_user.group,
            'date': one_unverified_user.created_at,
        })
     
    return jsonify({
        "unverified_users": data,
    }), HTTP_200_OK