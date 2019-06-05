from flask import Flask
from flask import jsonify, request, Response
from flask_cors import CORS
from pymongo import MongoClient
import random
from os import urandom
import json
import hashlib
import pickle
import pandas as pd


client = MongoClient('localhost', 27017)
db = client.rides_app_db

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

models = {'Alien Swirling Saucers':pickle.load(open('xgb_alien_saucers.pkl','rb')),
"Rock 'n' Roller Coaster":pickle.load(open('xgb_rock_n_rollercoaster.pkl','rb')),
"Slinky Dog Dash":pickle.load(open('xgb_slinky_dog.pkl','rb')),
"Toy Story Mania!":pickle.load(open('xgb_toy_story_mania.pkl','rb')),
"Avatar Flight of Passage":pickle.load(open('xgb_flight_of_passage.pkl','rb')),
"DINOSAUR":pickle.load(open('xgb_dinosaur.pkl','rb')),
"Expedition Everest":pickle.load(open('xgb_expedition_everest.pkl','rb')),
"Kilimanjaro Safaris":pickle.load(open('xgb_kilimanjaro_safaris.pkl','rb')),
"Na'vi River Journey":pickle.load(open('xgb_navi_river.pkl','rb')),
"Pirates of the Caribbean":pickle.load(open('xgb_pirates_of_caribbean.pkl','rb')),
"Seven Dwarfs Mine Train":pickle.load(open('xgb_dwarves.pkl','rb')),
"Spaceship Earth":pickle.load(open('xgb_spaceship_earth.pkl','rb')),
"Splash Mountain ":pickle.load(open('xgb_splash_mountain.pkl','rb')),
"Soarin":pickle.load(open('xgb_soarin.pkl','rb'))
}


@app.route("/api/parks", methods=["GET"])
def rides():
    rides_cursor = db.parks.find({}, {'_id': False})
    rides = []
    for ride in rides_cursor:
        rides.append(ride)
    return jsonify(rides)


@app.route("/api/predict", methods=["POST"])
def predict():
    request_json = request.get_json()
    print(request_json)
    # print(request_json['month'])
    # print(request_json['dayofweek'])
    wait_times = {}
    model = models[request_json['ride']]


    month= int(request_json['month'])
    day= int(request_json['day'])
    year= int(request_json['year'])
    hours = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0]
    minute= 0
    dayofweek= int(request_json['dayofweek'])

    for hour in hours:
        data = [[month, day, year, hour, minute, dayofweek]]
        input_df = pd.DataFrame(data, columns =['Month','Day','Year','Hour','Minute','DayOfWeek'])
        prediction = model.predict(input_df)
        wait_times[hour] = int(prediction[0])

    print(wait_times)
    return jsonify([
      {
        'name': '8am',
        'value': wait_times[8]
      },
      {
        'name': '9am',
        'value': wait_times[9]
      },
      {
        'name': '10am',
        'value': wait_times[10]
      },
      {
        'name': '11am',
        'value': wait_times[11]
      },
      {
        'name': '12pm',
        'value': wait_times[12]
      },
      {
        'name': '1pm',
        'value': wait_times[13]
      },
      {
        'name': '2pm',
        'value': wait_times[14]
      },
      {
        'name': '3pm',
        'value': wait_times[15]
      },
      {
        'name': '4pm',
        'value': wait_times[16]
      },
      {
        'name': '5pm',
        'value': wait_times[17]
      },
      {
        'name': '6pm',
        'value': wait_times[18]
      },
      {
        'name': '7pm',
        'value': wait_times[19]
      },
      {
        'name': '8pm',
        'value': wait_times[20]
      },
      {
        'name': '9pm',
        'value': wait_times[21]
      },
      {
        'name': '10pm',
        'value': wait_times[22]
      },
      {
        'name': '11pm',
        'value': wait_times[23]
      },
      {
        'name': '12am',
        'value': wait_times[0]
      }
    ])


@app.route("/api/create_user", methods=["POST"])
def create_user():
    request_json = request.get_json()
    users_cursor = db.users.find({}, {'_id': False})
    user_exists = False
    for user in users_cursor:
        if user['user_name'] == request_json['user_name']:
            user_exists = True
            break

    if user_exists:
        return Response(json.dumps({'status': 'user_exists'}), status=400, mimetype='application/json')
    else:
        password = request_json['password']
        password_hash = hashlib.md5(password.encode())
        password = password_hash.hexdigest()
        token = urandom(16).hex()
        token_hash = hashlib.md5(token.encode())
        token_hashed = token_hash.hexdigest()

        db.users.insert_one({
          'user_name': request_json['user_name'],
          'password': password,
          'favorite_rides': [],
          'recent_rides': [],
          'image': '',
          'token': token_hashed
        })
        return Response(json.dumps({'status': 'user_created', 'token': token}), status=200, mimetype='application/json')


@app.route("/api/login", methods=["POST"])
def login():
    request_json = request.get_json()
    users_cursor = db.users.find({}, {'_id': False})
    found_user = None
    for user in users_cursor:
        if user['user_name'] == request_json['user_name']:
            found_user = user
            break
    password = request_json['password']
    password_hash = hashlib.md5(password.encode())
    password = password_hash.hexdigest()
    if found_user and found_user['password'] == password:
        token = urandom(16).hex()
        token_hash = hashlib.md5(token.encode())
        token_hashed = token_hash.hexdigest()
        db.users.update_one(
            {'user_name': request_json['user_name']},
            {'$set': {
                'token': token_hashed
            }}
        )
        return Response(json.dumps({'status': 'successful', 'token': token}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'unsuccessful'}), status=401, mimetype='application/json')


@app.route("/api/logout", methods=["POST"])
def logout():
    token = request.headers.get('Authorization')
    token = token[7:]
    token_hash = hashlib.md5(token.encode())
    token_hashed = token_hash.hexdigest()
    users_cursor = db.users.find({}, {'_id': False})
    found_user = None
    for user in users_cursor:
        if user['token'] == token_hashed:
            found_user = user
            break

    if found_user:
        db.users.update_one(
            {'token': token_hashed},
            {'$set': {
                'token': ''
            }}
        )
        return Response(json.dumps({'status': 'successful'}), status=200,
                        mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'unsuccessful'}), status=401, mimetype='application/json')


@app.route("/api/user", methods=["GET"])
def get_user_info():
    token = request.headers.get('Authorization')
    token = token[7:]
    users_cursor = db.users.find({}, {'_id': False})
    found_user = None
    token_hash = hashlib.md5(token.encode())
    token_hashed = token_hash.hexdigest()
    for user in users_cursor:
        if user['token'] == token_hashed:
            found_user = user
            break

    if found_user:
        return Response(json.dumps({'status': 'successful', 'userName': found_user['user_name'],
                                    'image': found_user['image'], 'favorite_rides': found_user['favorite_rides'],
                                    'recent_rides': found_user['recent_rides']}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'unsuccessful'}), status=401, mimetype='application/json')


@app.route("/api/user", methods=["DELETE"])
def delete_user():
    token = request.headers.get('Authorization')
    token = token[7:]
    users_cursor = db.users.find({}, {'_id': False})
    found_user = None
    token_hash = hashlib.md5(token.encode())
    token_hashed = token_hash.hexdigest()
    for user in users_cursor:
        if user['token'] == token_hashed:
            found_user = user
            break

    if found_user:
        db.users.delete_one({'token': token_hashed})
        return Response(json.dumps({'status': 'successful'}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'unsuccessful'}), status=401, mimetype='application/json')


@app.route("/api/favorite_rides", methods=["POST"])
def set_favorite_rides():
    request_json = request.get_json()
    favorite_rides = request_json['favorite_rides']
    token = request.headers.get('Authorization')
    token = token[7:]
    users_cursor = db.users.find({}, {'_id': False})

    found_user = None
    token_hash = hashlib.md5(token.encode())
    token_hashed = token_hash.hexdigest()
    for user in users_cursor:
        if user['token'] == token_hashed:
            found_user = user
            break

    if found_user:
        db.users.update_one(
            {'token': token_hashed},
            {'$set': {
                'favorite_rides': favorite_rides
            }}
        )
        return Response(json.dumps({'status': 'successful', 'favoriteRides': found_user['favorite_rides']}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'unsuccessful'}), status=401, mimetype='application/json')


@app.route("/api/recent_rides", methods=["POST"])
def add_recent_ride():
    request_json = request.get_json()
    recent_ride = request_json['recent_ride']
    token = request.headers.get('Authorization')
    token = token[7:]
    users_cursor = db.users.find({}, {'_id': False})

    found_user = None
    token_hash = hashlib.md5(token.encode())
    token_hashed = token_hash.hexdigest()
    for user in users_cursor:
        if user['token'] == token_hashed:
            found_user = user
            break

    if found_user:
        recent_rides = found_user['recent_rides']
        if recent_ride in recent_rides:
            recent_rides.remove(recent_ride)
        recent_rides.append(recent_ride)
        if len(found_user['recent_rides']) > 5:
            recent_rides = recent_rides[1:]
        db.users.update_one(
            {'token': token_hashed},
            {'$set': {
                'recent_rides': recent_rides
            }}
        )
        return Response(json.dumps({'status': 'successful', 'recentRides': recent_rides}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'unsuccessful'}), status=401, mimetype='application/json')


@app.route("/api/user_image", methods=["POST"])
def set_user_image():
    print('hi')
    request_json = request.get_json()
    image = request_json['image']
    token = request.headers.get('Authorization')
    token = token[7:]
    users_cursor = db.users.find({}, {'_id': False})

    found_user = None
    token_hash = hashlib.md5(token.encode())
    token_hashed = token_hash.hexdigest()
    for user in users_cursor:
        if user['token'] == token_hashed:
            found_user = user
            break

    if found_user:
        db.users.update_one(
            {'token': token_hashed},
            {'$set': {
                'image': image
            }}
        )
        return Response(json.dumps({'status': 'successful'}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'unsuccessful'}), status=401, mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
