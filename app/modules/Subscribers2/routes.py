from datetime import datetime
from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import headers
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_SUBSCRIBER_COLLECTION2, MONGO_SERVERS_COLLECTION, MONGO_SUBSCRIBER_COLLECTION2
from flask import request, Blueprint, jsonify, render_template, escape, redirect, url_for

app = Blueprint('subscribers2', __name__)


@app.route('/subscribers2/datatable', methods=['GET'])
@headers
@login_required
def datatable_users2():
    try:
        mongo_client = mongoClient()
        col_subscribers = mongo_client[MONGO_DB][MONGO_SUBSCRIBER_COLLECTION2]

        datatable_data = {
            'data': list(col_subscribers.find({}, {'_id': 0, 'subscriber': 1, 'username': 1, 'password': 1, 'server': 1, 'created_at': 1, 'expires_at': 1,  'notes': 1}))
        }
        mongo_client.close()

        return jsonify(datatable_data) or [{}], 200
    except Exception as e:
        logger.exception(e)
        return [{}], 200


@app.route('/subscribers2', methods=['GET'])
@headers
@login_required
def subscribers_view2():
    try:
        mongo_client = mongoClient()
        col_servers = mongo_client[MONGO_DB][MONGO_SERVERS_COLLECTION]
        _server_data = list(col_servers.find({}, {'_id': 0, 'server': 1})) or []
        mongo_client.close()

        server_data = []
        for server in _server_data:
            server_data.append(server['server'])

        return render_template('subscriber2-management.html', csrf_token=CSRFClass().generate_CSRF(), server_data=server_data)

    except Exception as e:
        logger.exception(e)
        return render_template('subscriber2-management.html', csrf_token=CSRFClass().generate_CSRF())


@app.route('/subscribers2?<error_message>', methods=['GET'])
@headers
@login_required
def subscribers_error2(error_message=''):
    try:
        return render_template('subscriber2-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message=escape(error_message))

    except Exception as e:
        logger.exception(e)
        return render_template('subscriber2-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong, please try again!')


@app.route('/subscriber2/add', methods=['POST'])
@headers
@login_required
def add_subscriber2():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Please refresh the page and try again!'))

        subscriber = request.form['subscriber']
        username = request.form['username']
        password = request.form['password']
        server = request.form['server']
        expiration = request.form['expiration']
        notes = request.form['notes'] or ''

        if not subscriber or not username or not password or not server or not expiration:
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Please fill the form properly and try again!'))

        subscriber = escape(subscriber)
        username = escape(username)
        password = escape(password)
        server = escape(server)
        expiration = escape(expiration)
        notes = escape(notes)

        mongo_client = mongoClient()
        col_subscribers = mongo_client[MONGO_DB][MONGO_SUBSCRIBER_COLLECTION2]

        subscriber_exists = col_subscribers.find_one({'username': username}, {'_id': 0})
        if subscriber_exists:
            mongo_client.close()
            return redirect(url_for('subscribers2.subscribers_error2', error_message='A Subscriber with the same username already exists, try a different one!'))

        expiration = expiration.split('-')
        expiration = datetime(int(expiration[0]), int(expiration[1]), int(expiration[2]), 0, 0, 0, 0)

        added_subscriber = col_subscribers.insert_one({
            'subscriber': subscriber, 'username': username, 'password': password, 'server': server, 'created_at': datetime.now(), 'expires_at': expiration, 'notes': notes
        })
        mongo_client.close()

        if not added_subscriber.inserted_id:
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))

        return redirect(url_for('subscribers2.subscribers_view2'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))


@app.route('/subscriber2/edit', methods=['POST'])
@headers
@login_required
def edit_subscriber2():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Please refresh the page and try again!'))

        subscriber = request.form['subscriber']
        old_username = request.form['username_old']
        username = request.form['username']
        password = request.form['password']
        server = request.form['server']
        expiration = request.form['expiration']
        notes = request.form['notes'] or ''

        if not subscriber or not old_username or not username or not password or not server or not expiration:
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))

        subscriber = escape(subscriber)
        old_username = escape(old_username)
        username = escape(username)
        password = escape(password)
        server = escape(server)
        expiration = escape(expiration)
        notes = escape(notes)

        mongo_client = mongoClient()
        col_subscribers = mongo_client[MONGO_DB][MONGO_SUBSCRIBER_COLLECTION2]

        subscriber_exists = col_subscribers.find_one({'username': old_username}, {'_id': 0})
        if not subscriber_exists:
            mongo_client.close()
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))

        expiration = expiration.split('-')
        expiration = datetime(int(expiration[0]), int(expiration[1]), int(expiration[2]), 0, 0, 0, 0)

        col_subscribers.update_one({'username': old_username}, {'$set': {
            'subscriber': subscriber, 'username': username, 'password': password, 'server': server, 'expires_at': expiration, 'notes': notes
        }})
        mongo_client.close()

        return redirect(url_for('subscribers2.subscribers_view2'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))


@app.route('/subscriber2/delete', methods=['POST'])
@headers
@login_required
def subscriber_delete2():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Please refresh the page and try again!'))

        username = request.form['username']

        if not username:
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))

        username = escape(username)

        mongo_client = mongoClient()
        col_subscribers = mongo_client[MONGO_DB][MONGO_SUBSCRIBER_COLLECTION2]

        subscriber_deleted = col_subscribers.delete_one({'username': username})
        mongo_client.close()
        if not subscriber_deleted:
            return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))

        return redirect(url_for('subscribers2.subscribers_view2'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('subscribers2.subscribers_error2', error_message='Something went wrong, please try again!'))
