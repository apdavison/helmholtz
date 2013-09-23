'use strict';

/* Login Module */

angular.module( 'hermann.login', [
    'ngResource',
    'ngCookies',
])

/**
 * Module Routes
 * AngularJS will handle the merging
 * Controller for each route are managed in the corresponding <module>/controllers.js
 */
.config(
    function( $routeProvider ) {
        $routeProvider
        .when('/login', {
             templateUrl: 'login/form.tpl.html',   
             controller: LoginForm
        })
    }
)

/**
 * Function for creating new instances of the service model
 * containing as well the source of data and the methods to access it
 */
.factory( 
    'Login', // Object model
    function( $resource, $rootScope, $http, $location ){ // , $filter can be added if ngFilter is injected above
        // define 'Logout' function
        $rootScope.showLogout = false;
        $rootScope.removeAuthorization = function(){
            //remove default
            $rootScope.showLogout = false;
            $http.defaults.headers.common['Authorization'] = null;
            $location.path( '/login' );
        };
        // resource definition
        return $resource( base_url + '/people/researcher', { }, // try to access just to check answer
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
        });
    }
)

;
