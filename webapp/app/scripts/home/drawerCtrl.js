angular.module("lifebeltApp").controller("DrawerCtrl", function($scope, $mdSidenav) {
	"use strict";

	function exportMethods() {
		$scope.openDrawer = function() {
			$mdSidenav("sidenav-left").toggle();
		};
	}

	exportMethods();
});