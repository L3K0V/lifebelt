angular.module("lifebeltApp").config(function($stateProvider) {
	"use strict";

	$stateProvider.state("home.courses", {
		url: "courses",
		views: {
			"drawer@": {
				templateUrl: "scripts/courses/drawer.html",
				controller: "CoursesDrawerCtrl as coursesDrawerCtrl"
			},
			"header@": {
				templateUrl: "scripts/courses/header.html",
				controller: "CoursesHeaderCtrl as coursesHeaderCtrl"
			},
			"content@": {
				templateUrl: "scripts/courses/content.html",
				controller: "CoursesContentCtrl as coursesContentCtrl"
			}
		}
	});
});