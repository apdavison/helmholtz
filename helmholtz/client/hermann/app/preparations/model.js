'use strict';

/* Animals Module */

angular.module( 'hermann.preparations', ['ngResource'] )

/**
 * Module Routes
 * AngularJS will handle the merging
 * Controller for each route are managed in the corresponding <module>/controllers.js
 */
.config(
    function($routeProvider) {
        $routeProvider
        .when('/preparations/animal', {
             templateUrl: 'preparations/animal-list.tpl.html',   
             controller: ListAnimal
        })
        .when('/preparations/animal/:uri', {
             templateUrl: 'preparations/animal-detail.tpl.html', 
             controller: DetailAnimal
        })
        .when('/preparations/animal/edit/:uri', {
             templateUrl: 'preparations/animal-edit.tpl.html', 
             controller: EditAnimal
        })
    }
)

/**
 * Function for creating new instances of the service model
 * containing as well the source of data and the methods to access it
 */
.factory( 
    'Preparation', // Object model
    function( $resource ){ // , $filter can be added if ngFilter is injected above
        return $resource( base_url + ':uri', { uri:'@uri' },
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
            save: { method: 'POST', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
            del: { method: 'DELETE', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
        });
    }
)

.factory( 
    'Animal', // Object model
    function( $resource ){ // , $filter can be added if ngFilter is injected above
        return $resource( base_url + ':uri', { uri:'@uri' },
        {
            get: { method: 'GET', params:{ format:'json' }, isArray: false },
            save: { method: 'POST', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
            del: { method: 'DELETE', params:{ format:'json' }, headers:{ 'Content-Type':'application/json' } },
        });
    }
)

;
