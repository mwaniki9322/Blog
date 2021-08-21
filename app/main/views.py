from flask import render_template
from . import main


@main.route('/')
def index():
    '''
    view function for index page
    '''
    return render_template('index.html')