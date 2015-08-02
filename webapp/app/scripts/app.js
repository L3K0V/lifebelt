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
	"ngMaterial"
])
.config(function($urlRouterProvider, $mdThemingProvider) {
	$urlRouterProvider.when("", "/");
	$urlRouterProvider.otherwise("/404");

	$mdThemingProvider.theme('default').primaryPalette('indigo').accentPalette('pink');
});
