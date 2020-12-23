from flask import render_template, Blueprint, url_for

core = Blueprint('core', __name__, template_folder='templates/core')


@core.route('/')
def home():
    return render_template("home.html")


@core.route('/about')
def about():
    return render_template('about.html')


@core.route('/login')
def login():
    pass


@core.route('/logout')
def logout():
    pass
