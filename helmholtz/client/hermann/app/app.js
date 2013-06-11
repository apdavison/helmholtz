'use strict';

/**
 * This is our main app configuration file. 
 * It kickstarts the whole process by requiring all the modules from src/app that we need. 
 * We must load these now to ensure the routes are loaded. 
 * We only require the top-level module and allow the submodules to require their own submodules.
 */

// TODO: login module
var base_url = 'http://helm1/';
var auth = "Basic ZG86ZG8=";// until authentication form...

//var base_url = 'https://www.dbunic.cnrs-gif.fr/visiondb/';
//var auth = "Basic YW50b2xpa2phbjphamFu";

/* Main App Module */
angular.module( 'hermann', [ 
    //'hermann.filters', 
    //'hermann.services',
    'hermann.experiments',
    'hermann.researchers',
])

.config( 
    function( $httpProvider, $routeProvider ) {
        // http defaults
        $httpProvider.defaults.useXDomain = true;
        $httpProvider.defaults.headers.common['Authorization'] = auth;
        delete $httpProvider.defaults.headers.common['X-requested-With'];

        // defualt routing
        $routeProvider.otherwise({redirectTo: '/experiment'});
    }
)
;
