angular.module("lifebeltApp").controller("AssignmentsListCtrl", function(AssignmentsService) {
	"use strict";

	var controller = this;

	function initState() {
		AssignmentsService.getAssignments().then(function(assignments) {
			controller.assignments = assignments;
		});
	}

	function attachMethods() {
		controller.getTimeLeft = function(assignment) {
			return new Date(assignment.end) - new Date(assignment.start);
		};
	}

	initState();
	attachMethods();
});