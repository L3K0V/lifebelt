angular.module("lifebeltApp").controller("CourseOpenContentCtrl", function(CoursesService, $stateParams) {
	"use strict";

	var controller = this;
	
	function initState() {
		CoursesService.getCourse($stateParams.courseId).then(function(course) {
			controller.course = course;
		});
	}

	initState();
});