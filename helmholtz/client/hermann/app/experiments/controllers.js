'use strict';

/* Controllers */
//if minimizing: ExperimentDetailCtrl.$inject = ['$scope', '$routeParams', 'Experiment'];

function ListExperiment( $scope, Experiment )
{
    $scope.experiment = Experiment.get();
}

function DetailExperiment($scope, $routeParams, Experiment, People, Preparation, Animal ) 
{
    $scope.experiment = Experiment.get( {id: $routeParams.eId}, function(data){
        // when the exp is available, get researchers, to be expanded with another request
        $scope.researchers = new Array;
        $scope.experiment.researchers.forEach( function( entry ){
            var res = People.get( {uri: entry} );
            $scope.researchers.push( res );
        });
        // get preparation
        var preparation = Preparation.get({uri:$scope.experiment.preparation}, function(data){
            // when the preparation is available, get the animal
            $scope.animal = Animal.get({uri:preparation.animal});
        });
        // get setup
        //$scope.setup = ;
        // populate form from server:
        $scope.master_exp = angular.copy( $scope.experiment ); // default
    });
}

function EditExperiment($scope, $http, $routeParams, Experiment, People ) 
{
    DetailExperiment($scope, $routeParams, Experiment, People );
    // local update
    $scope.update = function( exp ){
        $scope.master_exp = angular.copy( exp );
        // check if something is changed
        // ...
        // save to server
        $scope.experiment.$save(); // removes trailing slash
    };
    // reset
    $scope.reset = function(){
        $scope.experiment = angular.copy( $scope.master_exp );
    };
    // reset
    $scope.delete = function( exp ){
        //$scope.experiment.$delete();
    };
}

