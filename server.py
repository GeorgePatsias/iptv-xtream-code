import config
from os import path, urandom
from flask_compress import Compress
from datetime import datetime, timedelta
from modules.Shared.Logger import logger
from modules.Shared.Headers import headers
from modules.Users.controllers import User
from modules.Shared.MongoClient import mongo_client
from flask_login import LoginManager, login_manager
from flask import Flask, send_from_directory, session, render_template


import modules.Login.routes
import modules.Users.routes
import modules.Streaming.routes
import modules.Dashboard.routes

app = Flask(__name__)
Compress(app)

app.register_blueprint(modules.Login.routes.app)
app.register_blueprint(modules.Users.routes.app)
app.register_blueprint(modules.Dashboard.routes.app)
app.register_blueprint(modules.Streaming.routes.app)


@app.route('/favicon.ico', methods=['GET'])
@headers
def favicon():
    return send_from_directory(path.join(app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html'), 404


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
        user_exists = col_admins.find_one({'username': username})
        if not user_exists:
            return

        user = User()
        user.id = username

        col_admins.update_one({'username': username}, {'$set': {'last_login': datetime.now()}})

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
    app.run(
        host=config.FLASK_HOST,
        port=config.FLAST_PORT,
        debug=config.FLASK_DEBUG,
        threaded=config.FLASK_THREADED
    )
