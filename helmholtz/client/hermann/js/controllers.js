'use strict';

/* Controllers */
//if minimizing: ExperimentDetailCtrl.$inject = ['$scope', '$routeParams', 'Experiment'];

function ExperimentListCtrl( $scope, Experiment )
{
    $scope.experiment = Experiment.query();
}

function ExperimentDetailCtrl($scope, $routeParams, Experiment ) 
{
    $scope.experiment = Experiment.query( {id: $routeParams.eId} );
}




/*
function ExperimentDetailCtrl($scope, $routeParams, $http ) 
{
    alert('route:'+$routeParams.eId);
    $http.get( 'http://helm1/experiments/'+ $routeParams.eId )
        .success( function( data ){
            alert( 'success' );
            $scope.experiment = data;
        })
        .error( function(){
            alert( 'error' );
        });
}
*/


/*
    //$scope.experiment = Experiment.get({id: $routeParams.id}, function(experiment) {
    //    //$scope.mainImageUrl = phone.images[0];
    //});

  $scope.phone = Phone.get({phoneId: $routeParams.phoneId}, function(phone) {
      $scope.mainImageUrl = phone.images[0];
  });

  $scope.setImage = function(imageUrl) {
      $scope.mainImageUrl = imageUrl; 
  }
*/
