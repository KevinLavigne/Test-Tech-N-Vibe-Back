# coding: utf-8
from flask import Flask,render_template, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import pandas as pd
from db.connection import *
from services.jwtEncode import *
from services.jwtDecode import *

app = Flask(__name__)

CORS(app,origins=["https://localhost:5173"], headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)

@app.route("/")
def index():
  return "try to connect to db"

@app.route('/login',  methods=['POST'])
def void():
  data = request.get_json()
  print(data)
  cur.execute('SELECT "email", "password" FROM "user" WHERE "email" = %s', (data["email"],) )
  result = cur.fetchone()
  print(result)
  if check_password_hash(result[1], data["password"]):
    token = encode_auth_token(result[0])
    response = make_response({"email": data["email"]},200)
    response.set_cookie("token", token, httponly = True, samesite="None",secure=True, max_age=63072000)
    return response
  return make_response({"type":"error","message":"invalid credential"},402)


@app.route('/signup', methods=['PUT'])
def signup():
  data = request.get_json()
  data["password"] = generate_password_hash(data["password"], method='pbkdf2:sha1', salt_length=8)
  cur.execute('INSERT INTO "user" (email, password) VALUES (%s,%s)', (data["email"],data["password"]))
  token = encode_auth_token(data["email"])
  response = make_response({"email": result[0], "token": token},200)
  response.set_cookie("token", token, httponly = True,samesite=None)
  return response

@app.route('/logout')
def logout():
  return 'Logout'


@app.route('/velib', methods = ['GET'])
def velib():

  if request.method == "GET" and Decode_auth_token(request.cookies.get("token")) is True:
    cur.execute('select latitude, longitude,"Nom de la station" AS stationName FROM velib_pos;')
    tmp = cur.fetchall()
    
# Extract the column names
    col_names = []
    for elt in cur.description:
      col_names.append(elt[0])
    return make_response(pd.DataFrame(tmp, columns=col_names).to_json(orient = "records"),200)
  return make_response({"type":"error","message":"unhautorized"},402)

@app.route('/velib/<latitude>/<longitude>', methods = ['GET'])
def velibNear(latitude, longitude):

  if request.method == "GET" and Decode_auth_token(request.cookies.get("token")) is True:
    print(latitude)
    print(longitude)
    cur.execute('select latitude, longitude,"Nom de la station" AS stationName, SQRT(POW(69.1 * (latitude - %s), 2) + POW(69.1 * (%s - longitude) * COS(latitude / 57.3), 2)) AS distance FROM velib_pos ORDER BY distance LIMIT 10;', [latitude, longitude])
    tmp = cur.fetchall()
    
# Extract the column names
    col_names = []
    for elt in cur.description:
      col_names.append(elt[0])
    return make_response(pd.DataFrame(tmp, columns=col_names).to_json(orient = "records"),200)
  return make_response({"type":"error","message":"unhautorized"},402)

if __name__=='__main__':
    app.run(debug = True)
