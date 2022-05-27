from datetime import datetime
from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.Headers import headers
from flask import Blueprint, render_template
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_SUBSCRIBER_COLLECTION

app = Blueprint('dashboard', __name__)


@app.route('/dashboard', methods=['GET'])
@headers
@login_required
def dashboard_view():
    try:
        mongo_client = mongoClient()
        col_subscribers = mongo_client[MONGO_DB][MONGO_SUBSCRIBER_COLLECTION]
        subscriber_data = list(col_subscribers.find({'expires_at': {'$gte': datetime.now()}}, {'_id': 0, 'created_at': 1}))
        mongo_client.close()

        data_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for item in subscriber_data:
            month = str(item.get('created_at')).split('-')[1]
            index = int(month) - 1

            count = data_list[index]
            data_list[index] = count + 1

        data_list = str(data_list).replace('[', '').replace(']', '')

        return render_template('dashboard.html', bar_chard_data=data_list)

    except Exception as e:
        logger.exception(e)
        return render_template('dashboard.html')
