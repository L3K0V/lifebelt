from flask import Flask, render_template, request, session

from flask.ext.github import GitHub
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager, login_required

from uuid import uuid4
from itsdangerous import URLSafeTimedSerializer

from .decorators import requires_roles

app = Flask(__name__)
app.config.from_object('config')

github = GitHub(app)
db = MongoEngine(app)

app.session_interface = MongoEngineSessionInterface(db)

login = LoginManager()
login.init_app(app)
login.session_protection = "strong"
login_serializer = URLSafeTimedSerializer(app.secret_key, salt=app.config['SESSION_SALT'])

from lifebelt.mod_users.models import User
from lifebelt.mod_users.controllers import mod_users as users_mod
from lifebelt.mod_courses.controllers import mod_courses as courses_mod
from lifebelt.mod_assignments.controllers import mod_assignments as assignments_mod

app.register_blueprint(users_mod)
app.register_blueprint(courses_mod)
app.register_blueprint(assignments_mod)


@app.route('/', methods=['GET'])
def index():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/admin')
@login_required
@requires_roles('admin')
def test_admin():
    return "<h1 style='color:red'>Hello ADMIN!</h1>"


@app.route('/teacher')
@login_required
@requires_roles('admin', 'teacher')
def test_teacher():
    return "<h1 style='color:red'>Hello TEACHER!</h1>"


@app.before_request
def _csrf_protect():
    if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
        csrf_token = session.pop('_csrf_token', None)
        if not csrf_token or csrf_token != request.json.get('_csrf_token'):
            abort(400)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid4())
    return session['_csrf_token']


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
