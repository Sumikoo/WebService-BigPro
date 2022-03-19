# Kelompok Big Project
# 1. Nur Khafidah (19090075) 6C
# 2. Helina Putri (19090133) 6D

# import library
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

# import library pendukung
import os
import jwt
import datetime

## inisialization object
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

## Configuration data base -----------------------------------------------------------
directory = os.path.dirname(os.path.abspath(__file__))
db_file = 'sqlite:///' + os.path.join(directory, "database/dbBigpro.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.config['SECRET_KEY'] = "appsecretkey"

## Schema Database Sqlite ------------------------------------------------------------
class UserAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(30))

db.create_all()


### Decorator Authentication ---------------------------------------------------------
def auth_on(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return make_response(jsonify({"msg":"Token not found !"}), 404)
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"Token invalid !"}))
        return f(*args, **kwargs)
    return decorator


### Routing Endpoint -----------------------------------------------------------------
# Routing Authentication
class RegisterUser(Resource):
    # posting data dari front-end untuk disimpan kedalam database
    def post(self):
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # checking username and password
        if fullname and username and email and password:
            user = UserAuth(fullname=fullname, username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            response = jsonify({"code":200,"msg":"Registration Complete !"})
            return response
        return jsonify({"msg":"Data tidak boleh kosong"})

# Routing Login
class LoginUser(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        # checking data
        query1 = [data.username for data in  UserAuth.query.all()]
        query2 = [data.password for data in  UserAuth.query.all()]

        if (username in query1) and (password in query2):
            token = jwt.encode({
                "username":query1, 
                "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm="HS256")
            return make_response(jsonify({"msg":"Login Successful !", "token": token}))
        return make_response(jsonify({"msg":"Login failed !"}))


# authentication page
class Dashboard(Resource):
    @auth_on
    def get(self):
        return jsonify({"msg":"Welcome! This is Dashboard with authentication"})

#### Resouce API List ----------------------------------------------------------------
api.add_resource(RegisterUser, "/api/register", methods=["POST"])
api.add_resource(LoginUser, "/api/login", methods=["POST"])
api.add_resource(Dashboard, "/api/dashboard", methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)