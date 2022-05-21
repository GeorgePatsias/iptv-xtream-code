# TODO RECAPTCHA https://python.plainenglish.io/how-to-use-google-recaptcha-with-flask-dbd79d5ea193
from uuid import uuid4
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Users.controllers import User
from modules.Shared.Headers import headers
from modules.Login.controllers import valid_user
from flask import Blueprint, render_template, request, redirect, escape
from flask_login import login_required, login_user, current_user, logout_user


app = Blueprint('login', __name__)


@app.route('/login', methods=['GET'])
@headers
def login_view():
    try:
        if current_user.is_authenticated:
            return redirect('/dashboard', code=302)

        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='')

    except Exception as e:
        logger.exception(e)
        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='*Invalid credentials!')


@app.route('/login', methods=['POST'])
@headers
def login_submit():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='*Please refresh the page and try again!')

        if current_user.is_authenticated:
            return redirect('/dashboard', code=302)

        if valid_user(request.form['username'], request.form['password']):
            authenticated_user = User()
            authenticated_user.id = escape(request.form['username'])
            authenticated_user.token = uuid4()
            login_user(authenticated_user, remember=False)

            return redirect('/dashboard', code=302)

        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='*Please refresh the page and try again!')

    except Exception as e:
        logger.exception(e)
        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='*Invalid credentials!')


@app.route('/logout', methods=['GET'])
@headers
@login_required
def logout():
    try:
        logout_user()
        return redirect('/login', code=302)

    except Exception as e:
        logger.exception(e)
        return redirect('/login', code=302)


@app.route('/test', methods=['GET'])
@headers
def test():
    from modules.Shared.MongoClient import mongo_client
    import config
    col_users = mongo_client[config.MONGO_DB][config.MONGO_USERS_COLLECTION]

    from werkzeug.security import generate_password_hash

    
    col_users.insert_one({'username': '3152673', 'password': '901859138', 'server': 'http://8kott.cx', 'created_at': "25/10/2022", 'expires_at': "25/10/2023", 'last_activity': "21/05/2022", 'notes': "My Notes here..."})
    return '', 200
