from datetime import datetime
from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import headers
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_SERVERS_COLLECTION
from flask import request, Blueprint, jsonify, render_template, escape, url_for, redirect

app = Blueprint('servers', __name__)


@app.route('/servers/datatable', methods=['GET'])
@headers
@login_required
def datatable_servers():
    try:
        mongo_client = mongoClient()
        col_servers = mongo_client[MONGO_DB][MONGO_SERVERS_COLLECTION]

        datatable_data = {
            'data': list(col_servers.find({}, {'_id': 0, 'server': 1, 'username': 1, 'password': 1, 'created_at': 1, 'notes': 1}))
        }
        mongo_client.close()

        return jsonify(datatable_data) or [{}], 200
    except Exception as e:
        logger.exception(e)
        return [{}], 200


@app.route('/servers', methods=['GET'])
@headers
@login_required
def servers_view():
    try:
        return render_template('servers-management.html', csrf_token=CSRFClass().generate_CSRF())

    except Exception as e:
        logger.exception(e)
        return render_template('servers-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong, please try again!')


@app.route('/server?<error_message>', methods=['GET'])
@headers
@login_required
def server_error(error_message=''):
    try:
        return render_template('servers-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message=escape(error_message))

    except Exception as e:
        logger.exception(e)
        return render_template('servers-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong, please try again!')


@app.route('/server/add', methods=['POST'])
@headers
@login_required
def server_add():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('servers.server_error', error_message='Please refresh the page and try again!'))

        server = request.form['server']
        username = request.form['username']
        password = request.form['password']
        notes = request.form['notes'] or ''

        if not server or not username or not password:
            return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))

        server = escape(server)
        username = escape(username)
        password = escape(password)
        notes = escape(notes)

        if str(server).endswith('/'):
            server = server[:-1]

        mongo_client = mongoClient()
        col_servers = mongo_client[MONGO_DB][MONGO_SERVERS_COLLECTION]

        server_exists = col_servers.find_one({'server': server, 'username': username}, {'_id': 0})
        if server_exists:
            mongo_client.close()
            return redirect(url_for('servers.server_error', error_message='A Server with the same URL and username already exists, try a different one!'))

        added_server = col_servers.insert_one({'server': server, 'username': username, 'password': password, 'created_at': datetime.now(), 'notes': notes})
        mongo_client.close()

        if not added_server.inserted_id:
            return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))

        return redirect(url_for('servers.servers_view'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))


@app.route('/server/delete', methods=['POST'])
@headers
@login_required
def server_delete():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('servers.server_error', error_message='Please refresh the page and try again!'))

        server = request.form['server']

        if not server:
            return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))

        server = escape(server)

        mongo_client = mongoClient()
        col_servers = mongo_client[MONGO_DB][MONGO_SERVERS_COLLECTION]

        server_deleted = col_servers.delete_one({'server': server})
        mongo_client.close()

        if not server_deleted:
            return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))

        return redirect(url_for('servers.servers_view'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))


@app.route('/server/edit', methods=['POST'])
@headers
@login_required
def edit_server():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('servers.server_error', error_message='Please refresh the page and try again!'))

        old_server = request.form['old_server']
        server = request.form['server']
        username = request.form['username']
        password = request.form['password']
        notes = request.form['notes'] or ''

        if not old_server or not server or not username or not password:
            return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))

        old_server = escape(old_server)
        server = escape(server)
        username = escape(username)
        password = escape(password)
        notes = escape(notes)

        mongo_client = mongoClient()
        col_servers = mongo_client[MONGO_DB][MONGO_SERVERS_COLLECTION]

        server_exists = col_servers.find_one({'server': old_server}, {'_id': 0})
        if not server_exists:
            mongo_client.close()
            return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))

        col_servers.update_one({'server': old_server}, {'$set': {'server': server, 'username': username, 'password': password, 'notes': notes}})
        mongo_client.close()

        return redirect(url_for('servers.servers_view'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('servers.server_error', error_message='Something went wrong, please try again!'))
