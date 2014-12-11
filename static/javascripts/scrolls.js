app = angular.module('scrolls', ['infinite-scroll']);

var ScrollsCtrl = function ($scope, $http) {
	$scope.name = 'Stefan';
	$scope.npcs = [
		[]
	];
	var lastIndex = 0;
	var totalCounter = 0;
	$scope.$evalAsync(function () {
		$scope.getNpcs();
	});

	$scope.getNpcs = function () {
		// $http.get('/npc', {
		// 	params: {
		// 		lores: true,
		// 		count: 9
		// 	}
		// });
		$http.get('/npc', {
			params: {
				// lores: true
			}
		}).then(function (response) {
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

	$scope.totalNpcs = function () {
		var total = 0;
		for (var i=0; i < $scope.npcs.length; i++) {
			total += $scope.npcs[i].length;
		}
		return total;
	}

	$scope.iconPlace = function (i, j) {
		var place = ((i-1)*3) + j;
		console.log(place);
		return place;
	}

	$scope.ghettoRange = function (num) {
		var newList = [];
		for (var i=0; i < num; i++) {
			newList.push(i+1);
		}
		return newList;
	}
};

app.controller(ScrollsCtrl);