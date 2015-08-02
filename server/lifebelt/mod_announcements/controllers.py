from lifebelt import db, login

from lifebelt.mod_courses.models import Course

from flask import Blueprint

mod_announcements = Blueprint('announcements', __name__, url_prefix='/courses')


@mod_assignments.url_defaults
def add_resources(endpoint, values):
    pass  # http://flask.pocoo.org/docs/0.10/patterns/urlprocessors/


@mod_assignments.url_value_preprocessor
def pull_resources(endpoint, values):
    pass  # http://flask.pocoo.org/docs/0.10/patterns/urlprocessors/


@mod_announcements.route('/<course_id>/announcements', methods=['GET'])
def get_all_course_announcements(course_id):
    pass


@mod_announcements.route('/<course_id>/announcements', methods=['POST'])
def create_new_course_announcement(course_id):
    pass


@mod_announcements.route('/<course_id>/announcements/<annon_id>', methods=['GET'])
def get_course_announcement(course_id, annon_id):
    pass


@mod_announcements.route('/<course_id>/announcements/<annon_id>', methods=['PUT'])
def edit_course_announcement(course_id, annon_id):
    pass


@mod_announcements.route('/<course_id>/announcements/<annon_id>', methods=['DELETE'])
def delete_course_announcement(course_id, annon_id):
    pass
