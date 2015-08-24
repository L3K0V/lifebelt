angular.module("lifebeltApp").service("AssignmentsService", function($state, Restangular) {
	"use strict";

	var service = this;

	function getAssignmentsEndpoint() {
		return Restangular.one("courses", $state.params.courseId);
	}

	function attachMethods() {
		service.getAssignments = function() {
			return getAssignmentsEndpoint().all("assignments").getList();
		};
		service.getAssignment = function(assignmentId) {
			return getAssignmentsEndpoint().one("assignment", assignmentId).get();
		};
	}

	attachMethods();
});