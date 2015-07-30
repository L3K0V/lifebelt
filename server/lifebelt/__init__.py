from flask import Flask
from flask import render_template

from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from .decorators import requires_roles

from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object('config')

github = GitHub(app)
db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)
login.session_protection = "strong"
login_serializer = URLSafeTimedSerializer(app.secret_key, salt=app.config['SESSION_SALT'])

from lifebelt.mod_users.models import User
from lifebelt.mod_users.controllers import mod_users as users_mod

app.register_blueprint(users_mod)

db.create_all()


@app.route('/', methods=['GET'])
def index():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/admin')
@requires_roles('admin')
def test_admin():
    return "<h1 style='color:red'>Hello ADMIN!</h1>"


@app.route('/teacher')
@requires_roles('admin', 'teacher')
def test_teacher():
    return "<h1 style='color:red'>Hello TEACHER!</h1>"


@app.errorhandler(401)
def unauthorized(error):
    return render_template("error.html", error='Unauthorized',
                           message='Login required...'), 401


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("error.html", error='Forbidden page',
                           message='You shall not pass.'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error='Page Not Found',
                           message='Sorry, but the page you were trying to view does not exist.'), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("error.html", error='Internal Server Error',
                           message='Something terribly wrong happened.'), 500
