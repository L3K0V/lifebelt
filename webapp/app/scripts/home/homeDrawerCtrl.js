angular.module("lifebeltApp").controller("HomeDrawerCtrl", function($state, $auth) {
	"use strict";

	var controller = this;

	function attachMethods() {
		controller.loginWithGithub = function() {
			$auth.authenticate("github", {
				state: "STATE"
			}).then(function() {
				console.log(arguments);
			});

		};
	}

	attachMethods();
});