angular.module("lifebeltApp").controller("LoggedinDrawerCtrl", function(LoginService) {
	"use strict";

	var controller = this;

	function initState() {
		LoginService.login().then(function(user) {
			controller.user = user;
		});
	}

	initState();
});