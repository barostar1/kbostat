from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('batter', __name__, url_prefix='/batterovr')


@bp.route('/', methods=['GET', 'POST'])
def batter():
    return render_template('batter.html')

