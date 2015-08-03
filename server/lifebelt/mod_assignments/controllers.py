from lifebelt import db, login

from lifebelt.mod_courses.models import Course
from lifebelt.mod_assignments.models import Assignment

from flask import g
from flask import Blueprint, request

from bson.json_util import loads, dumps

mod_assignments = Blueprint('assignments', __name__, url_prefix='/courses')


@mod_assignments.route('/<course_id>/assignments', methods=['GET'])
def get_all_course_assignments(course_id):
    c = Course.objects.get_or_404(id=course_id)
    json = loads(c.to_json())
    return dumps(json['assignments'])


@mod_assignments.route('/<course_id>/assignments', methods=['POST'])
def create_new_course_assignemnt(course_id):
    name = request.json.get('name')
    description = request.json.get('description')
    type = request.json.get('type')

    ass = Assignment()
    ass.name = name
    ass.description = description
    ass.type = type

    Course.objects.get_or_404(id=course_id).update_one(push__assignments=ass)

    return ass.to_json()


@mod_assignments.route('/<course_id>/assignments/<int:ass_index>', methods=['GET'])
def get_course_assignment_by_index(course_id, ass_index):
    return Course.objects.get_or_404(id=course_id).assignments[ass_index].to_json()


@mod_assignments.route('/<course_id>/assignemnts/<ass_index>', methods=['PUT'])
def edit_curse_assignemnt_by_index(course_id, ass_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_index>', methods=['DELETE'])
def delete_course_assignment_by_index(course_id, ass_id):
    pass


@mod_assignments.route('/<course_id>/assignments/<ass_id>/submissions', methods=['GET'])
def get_all_assignment_submissions(course_id, ass_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions', methods=['POST'])
def create_new_assignemnt_submission(course_id, ass_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>', methods=['GET'])
def get_assignment_submission(course_id, ass_id, sub_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>', methods=['PUT'])
def edit_assignment_submission(course_id, ass_id, sub_):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>', methods=['DELETE'])
def delete_assignment_submission(course_id, ass_id, sub_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/files', methods=['GET'])
def get_submission_files(course_id, ass_id, sub_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/files', methods=['POST'])
def attach_submission_file(course_id, ass_id, sub_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/status', methods=['GET'])
def get_submission_status(course_id, ass_id, sub_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/reviews', methods=['GET'])
def get_all_submission_reviews(course_id, ass_id, sub_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/reviews', methods=['POST'])
def create_new_submission_review(course_id, ass_id, sub_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/reviews/<rev_id>', methods=['GET'])
def get_submission_review(course_id, ass_id, sub_id, rev_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/reviews/<rev_id>', methods=['PUT'])
def edit_submission_review(course_id, ass_id, sub_id, rev_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>/submissions/<sub_id>/reviews/<rev_id>', methods=['DELETE'])
def delete_submission_review(course_id, ass_id, sub_id, rev_id):
    pass
