angular.module("lifebeltApp").config(function($stateProvider) {
	"use strict";

	$stateProvider.state("home.login", {
		url: "/login?code&state",
		views: {
			"content@": {
				controller: "LoginCtrl"
			}
		}
	});
});