import config
from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.Headers import headers
from modules.Users.controllers import valid_api
from modules.Shared.MongoClient import mongo_client
from flask import request, Blueprint, jsonify, render_template

app = Blueprint('users', __name__)


@app.route('/users', methods=['GET'])
@headers
@login_required
def users_view():
    try:

        return render_template('user-management.html')

    except Exception as e:
        logger.exception(e)
        return render_template('user-management.html')


@app.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()

    if not valid_api(data['api_key']):
        return {}, 401

    username = data.get('username', None)
    if not username:
        return {}, 400

    col_users = mongo_client()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    added_user = col_users.insert_one({
        "user_info": {
            "username": "8152748952",
            "password": "0012254179",
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
        },
        "server_info": {
            "url": "192.168.10.10",
            "port": "900",
            "https_port": "8080",
            "server_protocol": "http",
            "rtmp_port": "8081",
            "timezone": "UTC",
            "timestamp_now": 1651852719,
            "time_now": "2022-05-06 15:58:39",
            "process": True
        }
    })

    if not added_user.inserted_id:
        return {}, 400

    return {}, 200


@app.route('/user/edit', methods=['POST'])
def edit_user():
    data = request.get_json()

    if not valid_api(data['api_key']):
        return {}, 401

    #col_users = mongo_client()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    return '', 200


@app.route('/user/delete', methods=['POST'])
def delete_user():
    data = request.get_json()

    if not valid_api(data['api_key']):
        return {}, 401

    username = data.get('username', None)
    if not username:
        return {}, 400

    col_users = mongo_client()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]
    delete_user = col_users.delete_one({'user_info.username': username})

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

    col_users = mongo_client()[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    if username == 'all':
        user_data = list(col_users.find({}, {'_id': 0, 'user_info': 1}))

        return jsonify(user_data) or [{}], 200

    user_data = col_users.find_one({'user_info.username': username}, {'_id': 0, 'user_info': 1})

    return user_data or {}, 200


@app.route('/user/datatable', methods=['GET'])
@headers
@login_required
def datatable_users():
    col_users = mongo_client[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    datatable_data = {
        'data': list(col_users.find({}, {'_id': 0, 'username': 1, 'password': 1, 'server': 1, 'created_at': 1, 'expires_at': 1, 'last_activity': 1, 'notes': 1}))
    }

    return jsonify(datatable_data) or [{}], 200
