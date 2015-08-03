angular.module("lifebeltApp").controller("HomeDrawerCtrl", function($auth, $log) {
	"use strict";

	var controller = this;

	function attachMethods() {
		controller.loginWithGithub = function() {
			$auth.authenticate("github");
		};
	}

	attachMethods();
});