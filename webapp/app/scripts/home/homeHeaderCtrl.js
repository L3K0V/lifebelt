angular.module("lifebeltApp").controller("HomeHeaderCtrl", function($mdSidenav) {
	"use strict";

	var controller = this;

	function exportMethods() {
		controller.openDrawer = function() {
			$mdSidenav("sidenav-left").toggle();
		};
	}

	exportMethods();
});