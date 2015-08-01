from lifebelt import db, login

from flask import Blueprint

mod_assignments = Blueprint('assignments', __name__, url_prefix='/courses')


@mod_assignments.url_defaults
def add_resources(endpoint, values):
    pass  # http://flask.pocoo.org/docs/0.10/patterns/urlprocessors/


@mod_assignments.url_value_preprocessor
def pull_resources(endpoint, values):
    pass  # http://flask.pocoo.org/docs/0.10/patterns/urlprocessors/


@mod_assignments.route('/<course_id>/assignments', methods=['GET'])
def get_all_course_assignments(course_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts', methods=['POST'])
def create_new_course_assignemnt(course_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>', methods=['GET'])
def get_course_assignment(course_id, ass_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>', methods=['PUT'])
def edit_curse_assignemnt(course_id, ass_id):
    pass


@mod_assignments.route('/<course_id>/assignemnts/<ass_id>', methods=['DELETE'])
def delete_course_assignment(course_id, ass_id):
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
def get_submission_files(course_id, ass_id, sub_id):
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
