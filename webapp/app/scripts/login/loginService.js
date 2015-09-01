angular.module("lifebeltApp").service("LoginService", function(Restangular) {
	"use strict";

	var service = this;
	function attachMethods() {
		service.login = function(data) {
			return Restangular.all("auth").post(data);
		};
	}

	attachMethods();
});