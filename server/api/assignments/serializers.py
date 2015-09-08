from rest_framework import serializers, exceptions

from api.members.models import Member
from api.courses.models import Course

from api.assignments.models import CourseAssignment
from api.assignments.models import AssignmentSubmission
from api.assignments.models import SubmissionReview
from api.assignments.models import SubmissionFile


class CourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = CourseAssignment
        fields = ('id', 'name', 'description', 'assignment_type', 'submissions', 'start', 'end', 'target', 'date_created', 'date_modified')

    def create(self, validated_data):
        course = Course.objects.get(pk=self.context.get('course_pk'))

        assignment = CourseAssignment.objects.create(course=course, **validated_data)

        return assignment


class SubmissionFileSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Using HyperlinkedModelSerializer because we want to handle files as urls.
    '''
    class Meta:
        model = SubmissionFile
        read_only_fields = ('id', 'date_created', 'date_modified')
        fields = ('id', 'file', 'sha', 'date_created', 'date_modified')

    def create(self, validated_data):
        submission = AssignmentSubmission.objects.get(pk=self.context.get('submission_pk'))
        upload_file = self.context.get('request').data.get('file')

        upload = SubmissionFile.objects.create(submission=submission, file=upload_file)

        return upload


class SubmissionReviewSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SubmissionReview
        fields = ('id', 'author', 'description', 'points', 'date_created', 'date_modified')

    def create(self, validated_data):
        submission = AssignmentSubmission.objects.get(pk=self.context.get('submission_pk'))
        author = Member.objects.get(user=self.context.get('request').user)

        review = SubmissionReview.objects.create(submission=submission, author=author, **validated_data)

        return review


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
        files = SubmissionFileSerializer(many=True, read_only=True)
        reviews = SubmissionReviewSerializer(many=True, read_only=True)
        grade = serializers.IntegerField(min_value=0, max_value=100, default=0, required=False)

        author = serializers.PrimaryKeyRelatedField(read_only=True)

        class Meta:
            model = AssignmentSubmission
            fields = ('id', 'author', 'description', 'pull_request', 'files', 'reviews', 'grade', 'date_created', 'date_modified')

        def create(self, validated_data):
            assignment = CourseAssignment.objects.get(pk=self.context.get('assignment_pk'))
            author = Member.objects.get(user=self.context.get('request').user)
            submission = AssignmentSubmission.objects.create(assignment=assignment, author=author, **validated_data)

            return submission
