angular.module("lifebeltApp").config(function($stateProvider) {
	"use strict";

	$stateProvider.state("home.loggedin", {
		url: "",
		"abstract": true,
		views: {
			"drawer@": {
				templateUrl: "scripts/loggedin/drawer.html",
				controller: "LoggedinDrawerCtrl as loggedinDrawerCtrl"
			}
		}
	});
});