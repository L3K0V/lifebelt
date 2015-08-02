"use strict";
angular.module("lifebeltApp", [
	"ngAnimate",
	"ngCookies",
	"ngResource",
	"ngRoute",
	"ngSanitize",
	"ngTouch",
	"ui.router",
	"restangular",
])
.config(function($urlRouterProvider, $stateProvider) {
	$stateProvider.state("home", {
		url: "/",
		views: {
			"": {
				templateUrl: "scripts/frame/frame.html",
				controller: "MDLLoaderCtrl as mdlLoaderCtrl"
			},
			"drawer@home": {
				templateUrl: "scripts/frame/default-drawer.html"
			},
			"header@home": {
				templateUrl: "scripts/frame/default-header.html"
			},
			"content@home": {
				templateUrl: "scripts/frame/default-content.html"
			}
		}
	});

	$urlRouterProvider.when("", "/");
	$urlRouterProvider.otherwise("/404");
});
