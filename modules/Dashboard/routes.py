from flask_login import login_required
from modules.Shared.Logger import logger
from modules.Shared.Headers import headers
from flask import Blueprint, render_template

app = Blueprint('dashboard', __name__)


@app.route('/dashboard', methods=['GET'])
@headers
@login_required
def dashboard_view():
    try:

        return render_template('dashboard.html')

    except Exception as e:
        logger.exception(e)
        return render_template('dashboard.html')
