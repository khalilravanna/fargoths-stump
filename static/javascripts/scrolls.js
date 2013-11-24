app = angular.module('scrolls', ['infinite-scroll']);

function ScrollsCtrl ($scope, $http) {
	$scope.name = 'Stefan';
	$scope.npcs = [
		[]
	];
	var lastIndex = 0;
	var totalCounter = 0;
	$scope.$evalAsync(function () {
		$scope.getNpcs();
	});
	$scope.test = function () {
		console.log('sup');
	}
	$scope.getNpcs = function () {
		$http.get('/npc?lores=true').then(function (response) {
			if ($scope.npcs[lastIndex].length < 3) {
				$scope.npcs[lastIndex].push(response.data)
			}
			else {
				lastIndex++;
				$scope.npcs[lastIndex] = [response.data];
			}
			if (totalCounter < 8) {
				totalCounter++;
				console.log(totalCounter);
				$scope.getNpcs();
			}
		});
	};
}
app.controller(ScrollsCtrl)