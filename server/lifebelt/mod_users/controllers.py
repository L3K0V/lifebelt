from lifebelt import app, db, github
from lifebelt import login, login_serializer

from lifebelt.mod_users.models import User

from flask import Blueprint, request
from flask import jsonify, url_for
from flask.ext.login import current_user
from flask.ext.login import login_user, logout_user, login_required

from sqlalchemy import func

mod_users = Blueprint('users', __name__, url_prefix='/users')
login_manager = login


@app.route('/login', methods=['POST', 'GET'])
def login():
    if not current_user.is_authenticated():
        return github.authorize(scope="user, repo, admin:org")
    else:
        return '', 200


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return '', 204


@app.route('/me', methods=['GET'])
@login_required
def my_profile():
    return jsonify(current_user.to_json()), 200


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

        if db.session.query(func.count(User.id)).scalar() == 0:
            user.role = 'admin'

        db.session.add(user)
        db.session.commit()

    login_user(user)

    github_user = github.get('user')
    user.github = github_user['login']
    user.avatar_url = github_user['avatar_url']
    user.fullname = github_user['name']
    user.email = github_user['email']

    db.session.commit()

    data = user.to_json()
    data['token'] = user.get_auth_token()

    return jsonify(data), 201


@github.access_token_getter
def token_getter():
    if current_user.is_authenticated():
        return current_user.github_token


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@login_manager.request_loader
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


@mod_users.route('', methods=['GET'])
def get_all_users():
    pass


@mod_users.route('', methods=['POST'])
def create_user():
    pass


@mod_users.route('<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user(id):
    pass
