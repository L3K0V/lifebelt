angular.module("lifebeltApp").controller("HomeDrawerCtrl", function($state) {
	"use strict";

	var controller = this;

	function attachMethods() {
		controller.loginWithGithub = function() {
			// TODO
			// $auth.authenticate("github");

			$state.go("home.loggedin.courses");
		};
	}

	attachMethods();
});