angular.module("lifebeltApp").service("CoursesService", function(Restangular) {
	"use strict";

	var service = this;

	var coursesEndpoint = Restangular.all("courses");

	function attachMethods() {
		service.getCourses = function() {
			return coursesEndpoint.getList();
		};
		service.getCourse = function(courseId) {
			return coursesEndpoint.one(courseId).get();
		};
	}

	attachMethods();
});