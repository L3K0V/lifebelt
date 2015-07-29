'use strict';
angular.module('lifebeltApp', [
	'ngAnimate',
	'ngCookies',
	'ngResource',
	'ngRoute',
	'ngSanitize',
	'ngTouch',
	'ui.router',
	'restangular',
])
.config(function($urlRouterProvider, $stateProvider) {
	$stateProvider.state("home", {
		url: "/",
		views: {
			"": {
				templateUrl: 'scripts/frame/frame.html',
				controller: 'MDLLoaderCtrl as mdlLoaderCtrl'
			}
		}
	});

	$urlRouterProvider.when('', '/');
	$urlRouterProvider.otherwise("/404");
});
