'use strict';

/* App Module */

angular.module( 'notebook', [ 'notebookFilters', 'notebookServices' ])

    .config( ['$routeProvider', function($routeProvider) 
        {
            $routeProvider
                .when('/experiment', {
                    templateUrl: 'partials/experiment-list.html',   
                    controller: ExperimentListCtrl
                })
                .when('/experiment/:eId', {
                    templateUrl: 'partials/experiment-detail.html', 
                    controller: ExperimentDetailCtrl
                })
                .otherwise({redirectTo: '/experiment'});
        }
    ])

;
