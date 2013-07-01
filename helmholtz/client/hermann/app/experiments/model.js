'use strict';

/* Experiment Module */

angular.module( 'hermann.experiments', ['ngResource'] )

/**
 * Module Routes
 * AngularJS will handle the merging
 * Controller for each route are managed in the corresponding <module>/controllers.js
 */
.config(
    function($routeProvider) {
        $routeProvider
        .when('/experiment', {
             templateUrl: 'experiments/list.tpl.html',   
             controller: ListExperiment
        })
        .when('/experiment/:eId', {
             templateUrl: 'experiments/detail.tpl.html', 
             controller: DetailExperiment
        })
        .when('/experiment/:eId/edit', {
             templateUrl: 'experiments/edit.tpl.html', 
             controller: EditExperiment
        })
    }
)

/**
 * Function for creating new instances of the service model
 * containing as well the source of data and the methods to access it
 */
.factory( 
    'Experiment', // Object model
    function( $resource ){ // , $filter can be added if ngFilter is injected above
        return $resource( base_url + 'experiment/:id/', { id:'@eId' },
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
            save: { method: 'POST', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
            del: { method: 'DELETE', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
        });
    }
)

;
