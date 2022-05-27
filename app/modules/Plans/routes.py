from datetime import datetime
from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.Headers import headers
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_PLANS_COLLECTION
from flask import request, Blueprint, jsonify, render_template

app = Blueprint('plans', __name__)


@app.route('/plans/datatable', methods=['GET'])
@headers
@login_required
def datatable_plans():
    try:
        mongo_client = mongoClient()
        col_servers = mongo_client[MONGO_DB][MONGO_PLANS_COLLECTION]

        datatable_data = {
            'data': list(col_servers.find({}, {'_id': 0, 'server': 1, 'username': 1, 'password': 1, 'created_at': 1, 'notes': 1}))
        }
        mongo_client.close()

        return jsonify(datatable_data) or [{}], 200
    except Exception as e:
        logger.exception(e)
        return [{}], 200


@app.route('/plans', methods=['GET'])
@headers
@login_required
def plans_view():
    try:
        return render_template('plans-management.html', csrf_token=CSRFClass().generate_CSRF())

    except Exception as e:
        logger.exception(e)
        return render_template('plans-management.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong, please try again!')
