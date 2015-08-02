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
.config(function($urlRouterProvider) {
	$urlRouterProvider.when("", "/");
	$urlRouterProvider.otherwise("/404");
});
