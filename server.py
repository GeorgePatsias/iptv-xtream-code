import config
import requests
from os import urandom
from flask_compress import Compress
from MongoClient import mongoClient
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
Compress(app)


def valid_user(username='', password=''):
    try:
        col_users = mongoClient()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]
        if col_users.find_one({"user_info.username": username, "user_info.password": password}):
            mongoClient().close()
            return True
        mongoClient().close()
        return False

    except Exception:
        mongoClient().close()
        return False

def valid_api(api_key):
    try:
        if api_key == config.FLASK_API_KEY:
            return True
        return False
    except Exception:
        return False

@app.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()

    if not valid_api(data['api_key']):
        return {}, 401

    username = data.get('username', None)
    if not username:
        return {}, 400

    col_users = mongoClient()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    added_user = col_users.insert_one({
        "user_info": {
            "username": "1152748953",
            "password": "7012254178",
            "message": "Welcome To Best IPTV Service Provider",
            "auth": 1,
            "status": "Active",
            "exp_date": "1678790546",
            "is_trial": "0",
            "active_cons": "0",
            "created_at": "1647254546",
            "max_connections": "1",
            "allowed_output_formats": [
                "m3u8",
                "ts",
                "rtmp"
            ]
        }
    })

    mongoClient().close()

    if not added_user.inserted_id:
        return {}, 400

    return {}, 200

@app.route('/user/edit', methods=['POST'])
def edit_user():
    data = request.get_json()

    if not valid_api(data['api_key']):
        return {}, 401


    #col_users = mongoClient()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    return '', 200

@app.route('/user/delete', methods=['POST'])
def delete_user():
    data = request.get_json()

    if not valid_api(data['api_key']):
        return {}, 401

    username = data.get('username', None)
    if not username:
        return {}, 400

    col_users = mongoClient()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]
    delete_user = col_users.delete_one({'user_info.username' : username})
    mongoClient().close()

    if delete_user.deleted_count != 1:
        return {}, 400

    return {}, 200


@app.route('/user/show', methods=['POST'])
def show_user():
    data = request.get_json()

    if not valid_api(data['api_key']):
        return {}, 401

    username = data.get('username', None)
    if not username:
        return {}, 400

    col_users = mongoClient()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    if username == 'all':
        user_data = list(col_users.find({}, {'_id' : 0, 'user_info' : 1}))
        mongoClient().close()
        return jsonify(user_data) or [{}], 200

    user_data = col_users.find_one({'user_info.username' : username}, {'_id': 0, 'user_info' : 1})
    mongoClient().close()

    return user_data or {}, 200





@app.route('/player_api.php', methods=['GET'])
def player_api():
    if not valid_user(request.args.get('username', None), request.args.get('password', None)):
        return {}, 401

    response = requests.get("{}/player_api.php".format(config.API_URL), params=request.args, headers=request.headers, timeout=20)

    try:
        response_json = response.json()
        if response_json.get('server_info', None):
            response_json['server_info']['url'] = config.SERVER_IP
            response_json['server_info']['port'] = config.SERVER_PORT

            return response_json, response.status_code

    except Exception:
        pass

    return response.text or {}, response.status_code


@app.route('/xmltv.php', methods=['GET'])
def xmltv():
    try:
        parameters = request.args
        if not valid_user(parameters.get('username', None), parameters.get('password', None)):
            return {}, 401

        response = requests.get('{}/xmltv.php'.format(config.API_URL), headers=request.headers, params=parameters, timeout=20)

        return response.text or {}, response.status_code
    except Exception:
        return {}, 500


@app.route('/live/<username>/<password>/<stream_file>', methods=['GET'])
def live_stream(username, password, stream_file):
    if not valid_user(username, password):
        return {}, 401

    url = '{}/live/{}/{}/{}'.format(config.API_URL, username, password, stream_file)

    return redirect(url, code=301)


@app.route('/movie/<username>/<password>/<stream_file>', methods=['GET'])
def movie_stream(username, password, stream_file):
    if not valid_user(username, password):
        return {}, 401

    url = '{}/movie/{}/{}/{}'.format(config.API_URL, username, password, stream_file)

    return redirect(url, code=301)


@app.route('/series/<username>/<password>/<stream_file>', methods=['GET'])
def series_stream(username, password, stream_file):
    if not valid_user(username, password):
        return {}, 401

    url = '{}/series/{}/{}/{}'.format(config.API_URL, username, password, stream_file)

    return redirect(url, code=301)


if __name__ == '__main__':
    app.secret_key = urandom(60)
    app.run(
        host=config.FLASK_HOST,
        port=config.FLAST_PORT,
        debug=config.FLASK_DEBUG,
        threaded=config.FLASK_THREADED
    )
