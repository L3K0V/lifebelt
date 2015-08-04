from lifebelt import app, db, github, login, login_serializer

from lifebelt.mod_users.models import User

from flask import Blueprint, request, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user

from bson.json_util import loads, dumps

from datetime import datetime

mod_users = Blueprint('users', __name__, url_prefix='/users')
login_manager = login


@app.route('/login', methods=['POST', 'GET'])
def login():
    if not current_user.is_authenticated():
        return github.authorize(scope="user, repo, admin:org")
    else:
        return '', 200


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return '', 204


@app.route('/me', methods=['GET'])
@login_required
def my_profile():
    return current_user.to_json(), 200


@app.route('/github/callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or request.referrer or url_for('.index')
    if access_token is None:
        return redirect(next_url), 202

    user = User.objects(github_token=access_token).first()
    if user is None:
        user = User()
        user.github_token = access_token

        if len(User.objects) == 0:
            user.role = 'admin'
        user.save()

    login_user(user)

    github_user = github.get('user')
    user.github = github_user['login']
    user.avatar_url = github_user['avatar_url']
    user.fullname = github_user['name']
    user.email = github_user['email']

    user.save()

    print(user.get_auth_token())

    json = loads(user.to_json())
    json['token'] = user.get_auth_token()

    return dumps(json)


@github.access_token_getter
def token_getter():
    if current_user.is_authenticated():
        return current_user.github_token


@login_manager.user_loader
def load_user(userid):
    return User.objects.get_or_404(id=userid)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
        data = login_serializer.loads(token, max_age=max_age)
        user = User.objects.get_or_404(id=data[0])
        if user and user.github_token == data[1]:
            return user
    return None


@mod_users.route('', methods=['GET'])
def get_all_users():
    return User.objects.all().to_json()


@mod_users.route('', methods=['POST'])
def create_user():
    github = request.json.get('github')
    fullname = request.json.get('fullname')
    email = request.json.get('email')
    role = request.json.get('role') or 'student'
    s_grade = request.json.get('grade')
    s_class = request.json.get('class')
    s_number = request.json.get('number')

    user = User()
    user.github = github
    user.fullname = fullname
    user.email = email
    user.role = role
    user.details = {
        'class': s_class,
        'grade': s_grade,
        'number': s_number
    }

    user.save()
    return user.to_json(), 200


@mod_users.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    return User.objects.get_or_404(id=user_id).to_json()


@mod_users.route('/<user_id>', methods=['PUT'])
def edit_user(user_id):
    github = request.json.get('github')
    fullname = request.json.get('fullname')
    email = request.json.get('email')
    role = request.json.get('role') or 'student'
    s_grade = request.json.get('grade')
    s_class = request.json.get('class')
    s_number = request.json.get('number')

    user = User.objects.get_or_404(id=user_id)

    if github:
        user.update(github=github)
    if fullname:
        user.update(fullname=fullname)
    if email:
        user.update(email=email)
    if role:
        user.update(role=role)
    if s_grade:
        user.update(details__grade=s_grade)
    if s_class:
        user.update(details__class=s_class)
    if s_number:
        user.update(details__number=s_number)

    user.reload()

    return user.to_json(), 200


@mod_users.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.objects.get_or_404(id=user_id).delete()
    return '', 204
