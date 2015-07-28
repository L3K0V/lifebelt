from flask import Flask
from flask import render_template, session, request, redirect, url_for, abort
from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.config.from_object('config')

github = GitHub(app)
db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app)
login_serializer = URLSafeTimedSerializer(app.secret_key, salt=app.config['SESSION_SALT'])


@app.route('/', methods=['GET'])
def index():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/login/')
def login():
    if session.get('user_id', None) is None:
        return github.authorize(scope="user, repo, admin:org")
    else:
        return "200"


@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    return "204"


@app.route('/github/callback')
@github.authorized_handler
def authorized(access_token):
    print(access_token)
    return redirect(url_for('index', next=request.url))


@app.errorhandler(401)
def unauthorized(error):
    return render_template("error.html",
                           error='Unauthorized',
                           message='Login required...'), 401


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("error.html",
                           error='Forbidden page',
                           message='You shall not pass.'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error='Page Not Found',
                           message='Sorry, but the page you were trying to view does not exist.'), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("error.html",
                           error='Internal Server Error',
                           message='Something terribly wrong happened.'), 500
