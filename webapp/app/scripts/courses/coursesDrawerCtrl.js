angular.module("lifebeltApp").controller("CoursesDrawerCtrl", function() {
	"use strict";

	var controller = this;

	function initState() {
		// dummy data
		controller.username = "John Doe";
		controller.avatarUrl = "";
	}

	initState();
});
