from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.neuralstructures.api.resources import BrainRegionResource
from helmholtz.neuralstructures.api.resources import CellTypeResource
from helmholtz.neuralstructures.api.resources import CellResource
# instance
BrainRegion_resource = BrainRegionResource()
CellType_resource = CellTypeResource()
Cell_resource = CellResource()

urlpatterns = patterns('',

    url( r'^', include( BrainRegion_resource.urls ) ),
    url( r'^', include( CellType_resource.urls ) ),
    url( r'^', include( Cell_resource.urls ) ),

)
