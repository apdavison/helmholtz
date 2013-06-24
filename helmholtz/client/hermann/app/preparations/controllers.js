'use strict';

/* Controllers */
//if minimizing: ExperimentDetailCtrl.$inject = ['$scope', '$routeParams', 'Experiment'];

function ListAnimal( $scope, Animal )
{
    $scope.animal = Animal.get();
}

function DetailAnimal($scope, $routeParams, Animal, People ) 
{
    $scope.animal = Animal.get( {id: $routeParams.eId}, function(data){
        // get strain
        //$scope.strain = Strain.query();
        // get supplier
        $scope.supplier = People.get( {uri: $scope.animal.supplier} );
        // populate form from server:
        $scope.master_entry = angular.copy( $scope.animal ); // default
    });
}

function EditAnimal($scope, $http, $routeParams, Animal ) 
{
    DetailAnimal($scope, $routeParams, Animal );
    // local update
    $scope.update = function( entry ){
        $scope.master_entry = angular.copy( entry );
        // check if something is changed
        // ...
        // save to server
        $scope.animal.$save(); // removes trailing slash
    };
    // reset
    $scope.reset = function(){
        $scope.animal = angular.copy( $scope.master_entry );
    };
    // reset
    $scope.delete = function( entry ){
        //$scope.animal.$delete();
    };
}

