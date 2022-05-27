from os import path
from datetime import datetime, timedelta
from modules.Shared.Logger import logger
from modules.Shared.UserClass import User
from modules.Shared.Headers import headers
from modules.Shared.MongoClient import mongoClient
from flask_login import LoginManager, login_manager
from flask import Flask, send_from_directory, session, redirect
from config import MONGO_DB, MONGO_ADMINS_COLLECTION, SESSION_EXPIRE, FLASK_HOST, FLAST_PORT, FLASK_DEBUG, FLASK_THREADED, FLASK_SECRET


import modules.Login.routes
import modules.Plans.routes
import modules.Admins.routes
import modules.Servers.routes
import modules.Dashboard.routes
import modules.Subscribers.routes

app = Flask(__name__)
app.secret_key = FLASK_SECRET


app.register_blueprint(modules.Login.routes.app)
app.register_blueprint(modules.Plans.routes.app)
app.register_blueprint(modules.Admins.routes.app)
app.register_blueprint(modules.Servers.routes.app)
app.register_blueprint(modules.Dashboard.routes.app)
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
        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]
        admin_exists = col_admins.find_one({'username': username}, {'_id': 0, 'username': 1, 'locked': 1})
        if not admin_exists:
            mongo_client.close()
            return

        if admin_exists.get('locked') == 'true':
            return

        user = User()
        user.id = username

        col_admins.update_one({'username': username}, {'$set': {'last_activity': datetime.now()}})
        mongo_client.close()

        return user

    except Exception as e:
        logger.exception(e)
        mongo_client.close()
        return None


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=SESSION_EXPIRE)
    session.modified = True


if __name__ == '__main__':
    app.config.update(
        # SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        # SESSION_COOKIE_SAMESITE='None',
        SESSION_COOKIE_PATH='/',
        SESSION_COOKIE_NAME='Cookie'
    )

    app.run(
        host=FLASK_HOST,
        port=FLAST_PORT,
        debug=FLASK_DEBUG,
        threaded=FLASK_THREADED
    )
