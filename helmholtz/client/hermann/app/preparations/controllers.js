'use strict';

/* Controllers */
//if minimizing: ExperimentDetailCtrl.$inject = ['$scope', '$routeParams', 'Experiment'];

function ListAnimal( $scope, Animal )
{
    $scope.animal = Animal.get({uri:'preparations/animal'});
}

function DetailAnimal($scope, $routeParams, Animal, People, Strain ) 
{
    var path = 'preparations/animal/'+$routeParams.uri;
    $scope.animal = Animal.get( {uri: path}, function(data){
        // get strain
        $scope.strain = Strain.get({uri: $scope.animal.strain});
        // get supplier
        $scope.supplier = People.get( {uri: $scope.animal.supplier} );
        // populate form from server:
        $scope.master_entry = angular.copy( $scope.animal ); // default
    });
}

function EditAnimal($scope, $http, $routeParams, Animal, People, Strain ) 
{
    DetailAnimal($scope, $routeParams, Animal, People, Strain );
    // defaults
    $scope.birthCollapsed = true;
    $scope.sacrificeCollapsed = true;
    $scope.suppliers = People.get({uri:'people/supplier'});
    $scope.strains = Strain.get({uri:'species/strain'});
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

