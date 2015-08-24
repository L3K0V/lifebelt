angular.module("lifebeltApp").controller("LinkCtrl", function($scope, $state) {
	"use strict";

	function initScope() {
		$scope.goToState = function(state, params) {
			console.log("GO!");
			console.log(arguments);
			$state.go(state, params);
		};
	}

	initScope();
});