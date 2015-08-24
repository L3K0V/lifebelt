angular.module("lifebeltApp").filter("timeLeft", function() {
	"use strict";

	return function(start, end) { 
		return new Date(end) - new Date(start);
	};
});