'use strict';

/* Researcher Module */

angular.module( 'hermann.people', ['ngResource'] )
/*
.config(
    function($routeProvider) {
        $routeProvider
        .when('/researchers', {
             templateUrl: 'people/researcher-list.tpl.html',   
             controller: ListResearcher
        })
    }
)
*/

// since either researchers and supplier are accessed by their uri
// we only create the people object with different template
.factory( 
    'People', // Object model
    function( $resource ){ // , $filter can be added if ngFilter is injected above
        return $resource( base_url + ':uri', { uri:'@uri' },
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
        });
    }
)
/*
.factory( 
    'Researcher', // Object model
    function( $resource ){ // , $filter can be added if ngFilter is injected above
        return $resource( base_url + ':uri', { uri:'@uri' },
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
        });
    }
)

.factory( 
    'Supplier', // Object model
    function( $resource ){ // , $filter can be added if ngFilter is injected above
        return $resource( base_url + ':uri', { uri:'@uri' },
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
        });
    }
)
*/
;
