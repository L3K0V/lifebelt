angular.module("lifebeltApp").config(function($stateProvider) {
	"use strict";

	$stateProvider.state("home", {
		url: "/",
		views: {
			"": {
				templateUrl: "scripts/frame/frame.html",
				controller: "MDLLoaderCtrl as mdlLoaderCtrl"
			},
			"drawer@home": {
				templateUrl: "scripts/home/drawer.html"
			},
			"header@home": {
				templateUrl: "scripts/home/header.html"
			}
		}
	});
});