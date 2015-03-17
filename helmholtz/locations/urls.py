from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.locations.api.resources import PositionResource
# instance
Position_resource = PositionResource()

urlpatterns = patterns('',

    url( r'^', include( Position_resource.urls ) ),

)
