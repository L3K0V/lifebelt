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
		url: "/api/auth/login",
		clientId: "ac711ac25e851a667a11",
		redirectUri:  window.location.origin + "/static/index.html",
		type: "2.0",
		state: "STATE"
	});
	$authProvider.authToken = "Token";
});
