'use strict';

/* Controllers */
//if minimizing: ExperimentDetailCtrl.$inject = ['$scope', '$routeParams', 'Experiment'];

function ListExperiment( $scope, Experiment )
{
    $scope.experiment = Experiment.get();
}

function DetailExperiment($scope, $routeParams, Experiment, Researcher ) 
{
    $scope.experiment = Experiment.get( {id: $routeParams.eId}, function(data){
        // get researchers, to be expanded with another request
        $scope.researchers = new Array;
        $scope.experiment.researchers.forEach( function( entry ){
            var res = Researcher.query( {uri: entry} );
            $scope.researchers.push( res );
        });
        // get setup, already coming expanded by tastypie (if enabled)
        //$scope.setup = ;
        // get preparation, same as above
        //$scope.preparation = ;
        // populate form from server:
        $scope.master_exp = angular.copy( $scope.experiment ); // default
    });
}

function EditExperiment($scope, $http, $routeParams, Experiment, Researcher ) 
{
    DetailExperiment($scope, $routeParams, Experiment, Researcher );
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

