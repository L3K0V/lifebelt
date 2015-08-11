angular.module("lifebeltApp").controller("CoursesDrawerCtrl", function(LoginService) {
	"use strict";

	var controller = this;

	function initState() {
		LoginService.login().then(function(user) {
			console.log(user);
			controller.user = user;
		});
	}

	initState();
});
