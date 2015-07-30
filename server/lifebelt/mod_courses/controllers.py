from lifebelt import app, db
from lifebelt import login

from lifebelt.mod_courses.models import Course, CourseUser
from lifebelt.mod_users.models import User

from flask import Blueprint, request
from flask import jsonify, url_for
from flask.ext.login import current_user
from flask.ext.login import login_user, login_required

from ..decorators import requires_roles

from sqlalchemy import func

mod_courses = Blueprint('courses', __name__, url_prefix='/courses')
login_manager = login


@mod_courses.route('', methods=['GET'])
@login_required
def get_all_courses():
    return '', 500


@mod_courses.route('', methods=['POST'])
@login_required
@requires_roles('admin', 'teacher')
def create_course():
    initials = request.json.get('initials')
    fullname = request.json.get('fullname')
    description = request.json.get('description')
    year = request.json.get('year')

    toCreate = Course()

    if initials:
        toCreate.initials = initials
    if fullname:
        toCreate.fullname = fullname
    if description:
        toCreate.description = description
    if year:
        toCreate.year = year

    link = CourseUser(current_user, toCreate, user_role='teacher')

    db.session.add(toCreate)
    db.session.flush()

    db.session.add(link)
    db.session.commit()

    return jsonify(toCreate.to_json()), 200


@mod_courses.route('/<int:course_id>', methods=['GET'])
@login_required
def fetch_course(course_id):
        res = Course.query.filter_by(id=course_id).first()
        if res is None:
            return '', 404
        return jsonify(res.to_json())


@mod_courses.route('/<int:course_id>', methods=['PUT'])
@login_required
@requires_roles('admin', 'teacher')
def edit_course(course_id):
        initials = request.json.get('initials')
        fullname = request.json.get('fullname')
        description = request.json.get('description')
        year = request.json.get('year')

        toEdit = Course.query.filter_by(id=course_id).first()

        if toEdit:
            if initials:
                toEdit.initials = initials
            if fullname:
                toEdit.fullname = fullname
            if description:
                toEdit.description = description
            if year:
                toEdit.year = year

            db.session.commit()

            return jsonify(toEdit.to_json()), 200
        return '', 404


@mod_courses.route('/<int:course_id>', methods=['DELETE'])
@login_required
@requires_roles('admin', 'teacher')
def delete_course(course_id):
    toDelete = Course.query.filter_by(id=course_id).first()
    if toDelete:
        db.session.delete(toDelete)
        db.session.commit()
        return '', 204
    return 404


@mod_courses.route('/<int:course_id>/users', methods=['GET'])
def get_course_users(course_id):
    pass


@mod_courses.route('/<int:course_id>/users', methods=['POST'])
def add_user_to_course(course_id):
    pass
