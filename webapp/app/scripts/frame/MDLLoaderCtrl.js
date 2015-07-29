angular.module("lifebeltApp").controller("MDLLoaderCtrl", function($rootScope, $scope) {
	"use strict";

	function initState() {
		var offCallback = $rootScope.$on("$viewContentLoaded", function() {
			componentHandler.upgradeAllRegistered();
		});

		$scope.$on("$destroy", function() {
			offCallback();
		});
	}

	initState();
});