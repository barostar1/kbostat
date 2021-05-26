from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/kmain')
def kmain():
    return 'KBO 선수 오버롤'


@bp.route('/')
def index():
    return render_template('main.html')