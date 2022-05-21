import config
import requests
from flask import request, redirect, Blueprint
from modules.Streaming.controllers import valid_user

app = Blueprint('streaming', __name__)


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

    return redirect(url, code=308)


@app.route('/movie/<username>/<password>/<stream_file>', methods=['GET'])
def movie_stream(username, password, stream_file):
    if not valid_user(username, password):
        return {}, 401

    url = '{}/movie/{}/{}/{}'.format(config.API_URL, username, password, stream_file)

    return redirect(url, code=308)


@app.route('/series/<username>/<password>/<stream_file>', methods=['GET'])
def series_stream(username, password, stream_file):
    if not valid_user(username, password):
        return {}, 401

    url = '{}/series/{}/{}/{}'.format(config.API_URL, username, password, stream_file)

    return redirect(url, code=308)
