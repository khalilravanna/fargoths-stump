function ScrollsCtrl ($scope, $http, $timeout) {
	$scope.name = 'Stefan';
	$scope.npcs = [
		[]
	];
	var lastIndex = 0;

	$scope.$evalAsync(function () {
		myIntervalFunction();
	})

	var myIntervalFunction = function() {
	    cancelRefresh = $timeout(function myFunction() {
	    	$scope.getNPC();
	        cancelRefresh = $timeout(myFunction, 1000);
	    },1000);
	};
	console.log('Started.');

	$scope.getNPC = function () {
		console.log('Requesting NPC');
		$http.get('/npc').then(function (response) {
			console.log('Returned NPC');
			if ($scope.npcs[lastIndex].length < 3) {
				$scope.npcs[lastIndex].push(response.data)
			}
			else {
				lastIndex++;
				$scope.npcs[lastIndex] = [response.data];
			}
		});
	};
}