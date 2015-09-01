angular.module("lifebeltApp").controller("LoginCtrl", function($state, $stateParams, LoginService) {
	"use strict";

	function initState() {
		if(!$stateParams.code || !$stateParams.state) {
			$state.go("home");
		}

		LoginService.login({
			code: $stateParams.code,
			state: $stateParams.state
		}).then(function() {
			$state.go("home.loggedin");
		});
	}

	initState();
});