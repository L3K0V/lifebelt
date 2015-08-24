angular.module("lifebeltApp").config(function($stateProvider) {
	"use strict";

	$stateProvider
	.state("home.loggedin.courses", {
		url: "^/courses",
		views: {
			"header@": {
				templateUrl: "scripts/courses/header.html",
				controller: "CoursesHeaderCtrl as coursesHeaderCtrl"
			},
			"content@": {
				templateUrl: "scripts/courses/content.html",
				controller: "CoursesContentCtrl as coursesContentCtrl"
			}
		}
	})
	.state("home.loggedin.courses.open", {
		url: "/{courseId:[0-9]*}",
		views: {
			"header@": {
				templateUrl: "scripts/courses/open/header.html",
				controller: "CourseOpenHeaderCtrl as courseOpenHeaderCtrl"
			},
			"content@": {
				templateUrl: "scripts/courses/open/content.html",
				controller: "CourseOpenContentCtrl as courseOpenContentCtrl"
			}
		}
	})
	.state("home.loggedin.courses.open.assignments", {
		url: "/assignments",
		views: {
			"content@": {
				templateUrl: "scripts/assignments/content.html",
				controller: "AssignmentsListCtrl as assignmentsListCtrl"
			}
		}
	});
});