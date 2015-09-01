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
	"ngMaterial",
	"satellizer"
])
.config(function($urlRouterProvider, $mdThemingProvider, $authProvider, RestangularProvider) {
	$urlRouterProvider.when("", "/");
	$urlRouterProvider.otherwise("/404");

	RestangularProvider.setBaseUrl("../api");

	$mdThemingProvider.theme("default").primaryPalette("indigo").accentPalette("pink");

	$authProvider.github({
		url: "/login",
		clientId: "ac711ac25e851a667a11",
		redirectUri:  "http://0.0.0.0:8080/github/callback",
		type: "2.0"
	});
});
