from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.species.api.resources import SpeciesResource
from helmholtz.species.api.resources import StrainResource
# instance
species_resource = SpeciesResource()
strain_resource = StrainResource()

urlpatterns = patterns('',

    url( r'^', include( species_resource.urls ) ),
    url( r'^', include( strain_resource.urls ) ),

)
