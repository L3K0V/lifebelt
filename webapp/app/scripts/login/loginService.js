angular.module("lifebeltApp").service("LoginService", function(Restangular) {
	"use strict";

	var service = this;
	function attachMethods() {
		service.authenticate = function() {
			return Restangular.one("auth").one("me").get();
		};
	}

	attachMethods();
});