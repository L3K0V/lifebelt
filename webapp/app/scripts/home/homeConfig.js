angular.module("lifebeltApp").config(function($stateProvider) {
	"use strict";

	$stateProvider.state("home", {
		url: "/",
		views: {
			"drawer": {
				templateUrl: "scripts/home/drawer.html"
			},
			"header": {
				templateUrl: "scripts/home/header.html",
				controller: "HomeHeaderCtrl as homeHeaderCtrl"
			},
			"content": {
				templateUrl: "scripts/home/content.html"
			}
		}
	});
});