angular.module("lifebeltApp").controller("CoursesContentCtrl", function(CoursesService) {
	"use strict";

	var controller = this;

	function initState() {
		CoursesService.getCourses().then(function(courses) {
			controller.courses = courses;
		});
	}

	initState();
	
});