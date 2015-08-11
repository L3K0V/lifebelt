angular.module("lifebeltApp").service("LoginService", function(Restangular) {
	"use strict";

	var service = this;

	function attachMethods() {
		service.login = function() {
			return Restangular.one("login").post();
		};
	}


	attachMethods();
});