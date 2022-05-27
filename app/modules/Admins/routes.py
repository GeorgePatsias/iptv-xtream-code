from datetime import datetime
from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import headers
from modules.Shared.MongoClient import mongoClient
from werkzeug.security import generate_password_hash
from config import MONGO_DB, MONGO_ADMINS_COLLECTION
from flask import request, Blueprint, jsonify, render_template, escape, url_for, redirect

app = Blueprint('admins', __name__)


@app.route('/admins/datatable', methods=['GET'])
@headers
@login_required
def datatable_admins():
    try:
        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]

        datatable_data = {
            'data': list(col_admins.find({}, {'_id': 0, 'username': 1, 'created_at': 1, 'last_activity': 1, 'locked': 1}))
        }
        mongo_client.close()

        return jsonify(datatable_data) or [{}], 200

    except Exception as e:
        logger.exception(e)
        return [{}], 200


@app.route('/admins', methods=['GET'])
@headers
@login_required
def admins_view():
    try:
        return render_template('admins-management.html', csrf_token=CSRFClass().generate_CSRF())

    except Exception as e:
        logger.exception(e)
        return render_template('admins-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong, please try again!')


@app.route('/admins?<error_message>', methods=['GET'])
@headers
@login_required
def admins_error(error_message=''):
    try:
        return render_template('admins-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message=escape(error_message))

    except Exception as e:
        logger.exception(e)
        return render_template('admins-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong, please try again!')


@app.route('/admin/add', methods=['POST'])
@headers
@login_required
def admin_add():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('admins.admins_error', error_message='Please refresh the page and try again!'))

        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!'))

        username = escape(username)
        password = escape(password)

        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]

        admin_exists = col_admins.find_one({'username': username}, {'_id': 0})
        if admin_exists:
            mongo_client.close()
            return redirect(url_for('admins.admins_error', error_message='An Admin with the same username already exists, try a different one!'))

        added_admin = col_admins.insert_one({'username': username, 'password': generate_password_hash(password), 'created_at': datetime.now(), 'last_activity': '', 'locked': 'false'})
        mongo_client.close()
        if not added_admin.inserted_id:
            return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!'))

        return redirect(url_for('admins.admins_view'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!'))


@app.route('/admin/delete', methods=['POST'])
@headers
@login_required
def admin_delete():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('admins.admins_error', error_message='Please refresh the page and try again!'))

        username = request.form['username']

        if not username:
            return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!'))

        username = escape(username)

        if username == 'administrator':
            return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!'))

        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]

        admin_deleted = col_admins.delete_one({'username': username})
        mongo_client.close()
        if not admin_deleted:
            return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!'))

        return redirect(url_for('admins.admins_view'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!'))


@app.route('/admin/lock', methods=['POST'])
@headers
@login_required
def admin_lock():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return redirect(url_for('admins.admins_error', error_message='Please refresh the page and try again!4'))

        username = request.form['username']
        locked = request.form['locked']

        if not username or not locked:
            return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!3'))

        username = escape(username)
        locked = escape(locked)

        if username == 'administrator':
            return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!2'))

        if locked == 'false':
            locked = 'true'
        else:
            locked = 'false'

        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]
        col_admins.update_one({'username': username}, {'$set': {'locked': locked}})
        mongo_client.close()

        return redirect(url_for('admins.admins_view'))

    except Exception as e:
        logger.exception(e)
        return redirect(url_for('admins.admins_error', error_message='Something went wrong, please try again!1'))
