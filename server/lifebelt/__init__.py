from flask import Flask
from flask import render_template, session, request, redirect, url_for, abort, jsonify

from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, logout_user, current_user, login_user

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

db.create_all()


@login.user_loader
def load_user(userid):
    return User.query.get(userid)


@login.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
        data = login_serializer.loads(token, max_age=max_age)
        user = User.query.get(data[0])
        if user and user.github_token == data[1]:
            return user
    return None


@app.route('/', methods=['GET'])
def index():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/me', methods=['GET'])
@login_required
def my_profile():
    return jsonify(current_user.to_json()), 200


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize(scope="user, repo, admin:org")
    else:
        return '', 200


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '', 204


@app.route('/github/callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or request.referrer or url_for('index')
    if access_token is None:
        return redirect(next_url), 202

    user = User.query.filter_by(github_token=access_token).first()
    if user is None:
        user = User()
        user.github_token = access_token
        db.session.add(user)
        db.session.commit()

    login_user(user)
    data = user.to_json()
    data['token'] = user.get_auth_token()

    return jsonify(data), 201


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
