'use strict';

/* Login Controllers */
function getAllResearcherUser( $rootScope, People )
{
    // get all researchers
    $rootScope.allUsers = People.get( {uri:'people/user'}, function( data ){
        // upon arrival of users
        // effective researchers/users
        $rootScope.users = new Array;
        // for each of them get the user in order to have the name
        $rootScope.allUsers.objects.forEach( function( u ){
            $rootScope.allResearchers.objects.forEach( function( r ){
                //alert(u.resource_uri+' === '+r.user+')->'+(u.resource_uri===r.user));
                // when the researcher user matches user uri
                if( u.resource_uri == r.user ){
                    // create the option
                    var resuser = {
                        res_uri:  r.resource_uri,
                        user_uri: u.resource_uri,
                        name:     u.first_name+' '+u.last_name,
                        phone:    r.phone
                    };
                    $rootScope.users.push( resuser );
                }
            });
        });
        //alert( 'func:'+$rootScope.users.length);
    });
}

function LoginForm( $scope, $http, $location, $rootScope, Login, People )
{
    // set focus on username
    document.getElementById('username').focus();
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
        $rootScope.allResearchers = Login.get( {}, function( response, headers ){
            // match at rootscope, always available, the list of all researchers user-matched
            getAllResearcherUser( $rootScope, People );
            // continue to module
            if( headers('content-type').search('json') > 0 ){
                $rootScope.showLogout = true;
                $rootScope.username = username;
                $location.path( '/experiment' );
            }
        });
    };
}
