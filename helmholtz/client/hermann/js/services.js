'use strict';

var base_url = 'http://helm1/';
var auth = "Basic ZG86ZG8=";// until authentication form...

//var base_url = 'https://www.dbunic.cnrs-gif.fr/visiondb/';
//var auth = "Basic YW50b2xpa2phbjphamFu";

/* Services */

angular.module( 'notebookServices', ['ngResource'] )

    // configurations valid for all requests
    .config( ['$httpProvider', function( $httpProvider )
        {
            $httpProvider.defaults.useXDomain = true;
            $httpProvider.defaults.headers.common['Authorization'] = auth;
            delete $httpProvider.defaults.headers.common['X-requested-With'];
        }
    ])

    .factory( 'Experiment', function( $resource, $http ){ // , $filter can be added if ngFilter is injected above
            return $resource( base_url + 'experiment/:id/', { id:'@eId' },
            { 
                get: { method: 'GET', params:{ format:'json' }, isArray: false },
                save: { method: 'POST', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
                del: { method: 'DELETE', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
            }
        );
    })

    .factory( 'Researcher', function( $resource ){ // , $filter can be added if ngFilter is injected above
            return $resource( base_url + ':uri', { uri:'@uri' },
            { 
                get: { method: 'GET', params:{format:'json'}, isArray: false }
            }
        );
    })

;
