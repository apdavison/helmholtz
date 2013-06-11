'use strict';

/* Researcher Module */

angular.module( 'hermann.researchers', ['ngResource'] )
/*
.config(
    function($routeProvider) {
        $routeProvider
        .when('/researchers', {
             templateUrl: 'partials/experiment-list.html',   
             controller: ListExperiment
        })
    }
)
*/
.factory( 
    'Researcher', // Object model
    function( $resource ){ // , $filter can be added if ngFilter is injected above
        return $resource( base_url + ':uri', { uri:'@uri' },
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
        });
    }
)

;
