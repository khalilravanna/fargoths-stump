function ScrollsCtrl ($scope, $http) {
	$scope.name = 'Stefan';
	$scope.npcs = [
		[]
	];
	var lastIndex = 0;
	var totalCounter = 0;
	$scope.$evalAsync(function () {
		$scope.test();
	});
	$scope.test = function () {
		$http.get('/npc').then(function (response) {
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
				$scope.test();
			}
		});
	};
}