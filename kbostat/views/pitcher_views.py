from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
import pandas as pd
import csv

bp = Blueprint('pitcher', __name__, url_prefix='/pitcherovr')



@bp.route('/', methods=['GET', 'POST'])
def pitcher():
    return render_template('pitcher.html')

