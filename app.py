from ast import Return
from tkinter.messagebox import RETRY
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import jwt
import os
import datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database


class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password =  db.Column(db.String(100))


db.create_all()

# membuat routing enpoint
#routing auth
class RegisterUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword =  request.form.get('password')

        #cek username dan password
        if dataUsername and dataPassword:
            dataModel = AuthModel(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg": "Registrasy berhasil"}), 200)
        return jsonify({"msg": "Username/Password tidak boleh kosong"})

class LoginUser(Resource):
    def post(self):
        dataUsename = request.form.get('username')
        dataPassword =  request.form.get('password')

        #query mach
        query= [data.username for data in AuthModel.query.all()]
        if dataUsename in query:
            return jsonify({"msg": "Login sukses"})

        return jsonify({"msg": "Login gagal, silakan coba lagi!!!"})

#resource api
api.add_resource(RegisterUser, "/api/register", methods=["POST"])
api.add_resource(LoginUser, "/api/login", methods=["POST"])

if __name__=="__main__":
    app.run(debug=True)
