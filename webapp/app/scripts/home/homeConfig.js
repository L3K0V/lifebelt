angular.module("lifebeltApp").config(function($stateProvider) {
	"use strict";

	$stateProvider.state("home", {
		url: "/",
		views: {
			"drawer": {
				templateUrl: "scripts/home/drawer.html",
				controller: "HomeDrawerCtrl as homeDrawerCtrl"
			},
			"header": {
				templateUrl: "scripts/home/header.html"
			},
			"content": {
				templateUrl: "scripts/home/content.html"
			}
		}
	});
});