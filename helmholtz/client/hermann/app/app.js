'use strict';

/**
 * This is our main app configuration file. 
 * It kickstarts the whole process by requiring all the modules from src/app that we need. 
 * We must load these now to ensure the routes are loaded. 
 * We only require the top-level module and allow the submodules to require their own submodules.
 */

var base_url = 'http://helm1/';
//var base_url = 'https://www.dbunic.cnrs-gif.fr/visiondb/';

/* Main App Module */
angular.module( 'hermann', [ 
    //'ui.bootstrap',
    //'hermann.filters', 
    //'hermann.services',
    'hermann.login', 
    'hermann.experiments',
    'hermann.researchers',
])

.config(  
    function( $httpProvider, $routeProvider, $locationProvider ) {
        // http defaults
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-requested-With'];

        // defualt routing
        $routeProvider.otherwise({redirectTo: '/experiment'});

        // Login
        // intercept http 401 error and redirect to login page
        var HttpErrorInterceptor = ['$location', function( $location ) {
            function success( response ) {
                return response;
            }
            function error( response ) {
                // show login
                if (response.status === 401 ) {
                    alert("Authentication Failure");
                    $location.path( '/login' );
                }
                return response;
            }
            return function( promise ) {
                return promise.then( success, error );
            }
        }];
        $httpProvider.responseInterceptors.push( HttpErrorInterceptor );
    }
)

;
