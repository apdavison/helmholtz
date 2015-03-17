from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.preparations.api.resources import AnimalResource
from helmholtz.preparations.api.resources import PreparationResource
# instance
Animal_resource = AnimalResource()
Preparation_resource = PreparationResource()

urlpatterns = patterns('',

    url( r'^', include( Animal_resource.urls ) ),
    url( r'^', include( Preparation_resource.urls ) ),

)
