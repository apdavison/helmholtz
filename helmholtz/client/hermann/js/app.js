'use strict';

/* App Module */

angular.module( 'notebook', [ 'notebookFilters', 'notebookServices' ])

    .config( ['$routeProvider', function($routeProvider) 
        {
            $routeProvider
                .when('/experiment', {
                    templateUrl: 'partials/experiment-list.html',   
                    controller: ListExperiment
                })
                .when('/experiment/:eId', {
                    templateUrl: 'partials/experiment-detail.html', 
                    controller: DetailExperiment
                })
                .when('/experiment/edit/:eId', {
                    templateUrl: 'partials/experiment-edit.html', 
                    controller: EditExperiment
                })
                .otherwise({redirectTo: '/experiment'});
        }
    ])

;
