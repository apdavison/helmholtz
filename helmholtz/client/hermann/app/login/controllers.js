'use strict';

/* Login Controllers */

function LoginForm( $scope, $http, $location, $rootScope, Login )
{
    // the controller declares a function used onclick submit
    $scope.submitLogin = function(){
        // retrieve login form data
        var username = $scope.username;
        var password = $scope.password;
        // encode base64
        var userpass64 = btoa( username+':'+password );
        // assign default Authorization header
        $http.defaults.headers.common['Authorization'] = "Basic " + userpass64;
        // send message to check
        Login.get( {}, function( response, headers ){
            //alert( headers('content-type') );
            if( headers('content-type').search('json') > 0 ){
                $rootScope.showLogout = true;
                $location.path( '/experiment' );
            }
        });
    };
}
