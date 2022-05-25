import config
from os import path, urandom
from flask_compress import Compress
from datetime import datetime, timedelta
from modules.Shared.Logger import logger
from modules.Shared.UserClass import User
from modules.Shared.Headers import headers
from modules.Shared.MongoClient import mongo_client
from flask_login import LoginManager, login_manager
from flask import Flask, send_from_directory, session, redirect


import modules.Login.routes
import modules.Admins.routes
import modules.Servers.routes
import modules.Streaming.routes
import modules.Dashboard.routes
import modules.Subscribers.routes

app = Flask(__name__)
Compress(app)


app.register_blueprint(modules.Login.routes.app)
app.register_blueprint(modules.Admins.routes.app)
app.register_blueprint(modules.Servers.routes.app)
app.register_blueprint(modules.Dashboard.routes.app)
app.register_blueprint(modules.Streaming.routes.app)
app.register_blueprint(modules.Subscribers.routes.app)


@app.route('/favicon.ico', methods=['GET'])
@headers
def favicon():
    return send_from_directory(path.join(app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/login'), 308


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = (u"Session time out, please re-login")
login_manager.needs_refresh_message_category = "info"


@login_manager.user_loader
def load_user(username):
    try:
        col_admins = mongo_client[config.MONGO_DB][config.MONGO_ADMINS_COLLECTION]
        admin_exists = col_admins.find_one({'username': username}, {'_id': 0, 'username': 1, 'locked': 1})
        if not admin_exists:
            return

        if admin_exists.get('locked') == 'true':
            return

        user = User()
        user.id = username

        col_admins.update_one({'username': username}, {'$set': {'last_activity': datetime.now()}})

        return user
    except Exception as e:
        logger.exception(e)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=config.SESSION_EXPIRE)
    session.modified = True


if __name__ == '__main__':
    app.secret_key = urandom(60)

    app.config.update(
        # SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        # SESSION_COOKIE_SAMESITE='None',
        SESSION_COOKIE_PATH='/',
        SESSION_COOKIE_NAME='Cookie'
    )

    app.run(
        host=config.FLASK_HOST,
        port=config.FLAST_PORT,
        debug=config.FLASK_DEBUG,
        threaded=config.FLASK_THREADED
    )
