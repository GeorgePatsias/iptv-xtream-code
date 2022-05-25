import config
import requests
from datetime import datetime
from modules.Shared.Logger import logger
from modules.Shared.MongoClient import mongo_client
from flask import request, redirect, Blueprint, Response
from modules.Streaming.controllers import valid_subscriber

app = Blueprint('streaming', __name__)


@app.route('/player_api.php', methods=['GET'])
def player_api():
    try:
        subscriber_server, server_username, server_password = valid_subscriber(request.args.get('username', None), request.args.get('password', None))

        if not subscriber_server or not server_username or not server_password:
            return {}, 401

        username = request.args.get('username')
        password = request.args.get('password')

        col_subscribers = mongo_client[config.MONGO_DB][config.MONGO_SUBSCRIBER_COLLECTION]
        col_subscribers.update_one({'username': username, 'password': password}, {'$set': {'last_activity': datetime.now()}})

        request_arguments = request.args.copy()
        request_arguments['username'] = server_username
        request_arguments['password'] = server_password

        response = requests.get('{}/player_api.php'.format(subscriber_server), params=request_arguments, headers=request.headers, timeout=20)

        try:
            response_json = response.json()

            if response_json.get('server_info', None) and response_json.get('user_info', None):
                response_json['user_info']['username'] = username
                response_json['user_info']['password'] = password
                response_json['server_info']['url'] = config.STREAMFLIX_SERVER_IP
                response_json['server_info']['port'] = config.STREAMFLIX_SERVER_PORT

                return response_json, response.status_code

        except Exception:
            pass

        return response.text or {}, response.status_code
    except Exception as e:
        logger.exception(e)
        return {}, 500


@app.route('/xmltv.php', methods=['GET'])
def xmltv():
    try:
        subscriber_server, server_username, server_password = valid_subscriber(request.args.get('username', None), request.args.get('password', None))

        if not subscriber_server or not server_username or not server_password:
            return {}, 401

        request_arguments = request.args.copy()
        request_arguments['username'] = server_username
        request_arguments['password'] = server_password

        response = requests.get('{}/xmltv.php'.format(subscriber_server), headers=request.headers, params=request_arguments, timeout=20)

        return response.text or {}, response.status_code
    except Exception:
        return {}, 500


# @app.route('/movie/<username>/<password>/<stream_file>', methods=['GET'])
# def movie_stream(username, password, stream_file):
#     subscriber_server, server_username, server_password = valid_subscriber(request.args.get('username', None), request.args.get('password', None))

#     if not subscriber_server or not server_username or not server_password:
#         return {}, 401

#     url = '{}/movie/{}/{}/{}'.format(subscriber_server, username, password, stream_file)

#     return redirect(url, code=302)

@app.route('/movie/<username>/<password>/<stream_file>', methods=['GET'])
def movie_stream(username, password, stream_file):
    subscriber_server, server_username, server_password = valid_subscriber(username, password)

    if not subscriber_server or not server_username or not server_password:
        return {}, 401

    request_arguments = request.args.copy()
    request_arguments['username'] = server_username
    request_arguments['password'] = server_password

    url = '{}/movie/{}/{}/{}'.format(subscriber_server, username, password, stream_file)

    response = requests.get(url, headers=request.headers, params=request_arguments, stream=True)

    return Response(response.iter_content(chunk_size=config.STREAMING_CHUNK_SIZE), content_type=response.headers['Content-Type'])


# @app.route('/series/<username>/<password>/<stream_file>', methods=['GET'])
# def series_stream(username, password, stream_file):
#     subscriber_server, server_username, server_password = valid_subscriber(request.args.get('username', None), request.args.get('password', None))

#     if not subscriber_server or not server_username or not server_password:
#         return {}, 401

#     url = '{}/series/{}/{}/{}'.format(subscriber_server, username, password, stream_file)

#     return redirect(url, code=302)

@app.route('/series/<username>/<password>/<stream_file>', methods=['GET'])
def series_stream(username, password, stream_file):
    subscriber_server, server_username, server_password = valid_subscriber(username, password)

    if not subscriber_server or not server_username or not server_password:
        return {}, 401

    request_arguments = request.args.copy()
    request_arguments['username'] = server_username
    request_arguments['password'] = server_password

    url = '{}/series/{}/{}/{}'.format(subscriber_server, username, password, stream_file)
    response = requests.get(url, headers=request.headers, params=request_arguments, stream=True)

    return Response(response.iter_content(chunk_size=config.STREAMING_CHUNK_SIZE), content_type=response.headers['Content-Type'])

# @app.route('/live/<username>/<password>/<stream_file>', methods=['GET'])
# def live_stream(username, password, stream_file):
#     subscriber_server, server_username, server_password = valid_subscriber(username, password)

#     if not subscriber_server or not server_username or not server_password:
#         return {}, 401

#     url = '{}/live/{}/{}/{}'.format(subscriber_server, server_username, server_password, stream_file)

#     return redirect(url, code=302)


@app.route('/live/<username>/<password>/<stream_file>', methods=['GET'])
def live_stream(username, password, stream_file):
    subscriber_server, server_username, server_password = valid_subscriber(username, password)

    if not subscriber_server or not server_username or not server_password:
        return {}, 401

    request_arguments = request.args.copy()
    request_arguments['username'] = server_username
    request_arguments['password'] = server_password

    url = '{}/live/{}/{}/{}'.format(subscriber_server, server_username, server_password, stream_file)

    response = requests.get(url, headers=request.headers, params=request_arguments, stream=True)
    return Response(response.iter_content(chunk_size=config.STREAMING_CHUNK_SIZE), content_type=response.headers['Content-Type'])
