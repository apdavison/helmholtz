from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.units.api.resources import UnitResource

# instance
unit_resource = UnitResource()

urlpatterns = patterns('',

    url( r'^', include( unit_resource.urls ) ),

)
