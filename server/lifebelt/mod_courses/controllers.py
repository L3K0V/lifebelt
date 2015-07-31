from lifebelt import db, login

from lifebelt.mod_courses.models import Course
from lifebelt.mod_users.models import User

from flask import Blueprint, request
from flask.ext.login import current_user, login_required

from datetime import datetime

from ..decorators import requires_roles

mod_courses = Blueprint('courses', __name__, url_prefix='/courses')
login_manager = login


@mod_courses.route('', methods=['GET'])
@login_required
def get_all_courses(page=1):
    return Course.objects.all().to_json()


@mod_courses.route('', methods=['POST'])
@login_required
def create_course():
    initials = request.json.get('initials')
    fullname = request.json.get('fullname')
    description = request.json.get('description')
    year = request.json.get('year') or datetime.now().year

    toCreate = Course()

    if initials:
        toCreate.initials = initials
    if fullname:
        toCreate.fullname = fullname
    if description:
        toCreate.description = description

    toCreate.year = year
    toCreate.users = [{
        'user': current_user.id,
        'role': 'teacher'
    }]

    toCreate.save()
    User.objects(id=current_user.id).update_one(push__courses=toCreate)

    return toCreate.to_json(), 200


@mod_courses.route('/<course_id>', methods=['GET'])
@login_required
def fetch_course(course_id):
        res = Course.objects.get_or_404(id=course_id)
        return res.to_json()


@mod_courses.route('/<course_id>', methods=['PUT'])
@login_required
@requires_roles('admin', 'teacher')
def edit_course(course_id):
        initials = request.json.get('initials')
        fullname = request.json.get('fullname')
        description = request.json.get('description')
        year = request.json.get('year')

        toEdit = Course.objects.get_or_404(id=course_id)

        if initials:
            toEdit.update(initials=initials)
        if fullname:
            toEdit.update(fullname=fullname)
        if description:
            toEdit.update(description=description)
        if year:
            toEdit.update(year=year)

        toEdit.update(date_modified=datetime.now)
        toEdit.reload()

        return toEdit.to_json(), 200


@mod_courses.route('/<course_id>', methods=['DELETE'])
@login_required
@requires_roles('admin', 'teacher')
def delete_course(course_id):
    Course.objects.get(id=course_id).delete()
    return '', 204


@mod_courses.route('/<course_id>/users', methods=['GET'])
def get_course_users(course_id):
    res = Course.objects.get_or_404(id=course_id)
    return User.objects(courses__in=[res]).to_json()

    # Query all courses for user
    # res = User.objects.get_or_404(id=course_id)
    # return Course.objects(users__user__in=[res.id]).to_json()


@mod_courses.route('/<course_id>/users', methods=['POST'])
def add_user_to_course(course_id):
    pass
