from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.people.api.resources import UserResource
from helmholtz.people.api.resources import ResearcherResource
from helmholtz.people.api.resources import ScientificStructureResource
from helmholtz.people.api.resources import PositionResource
from helmholtz.people.api.resources import SupplierResource
# instance
user_resource = UserResource()
researcher_resource = ResearcherResource()
scientific_resource = ScientificStructureResource()
position_resource = PositionResource()
supplier_resource = SupplierResource()

urlpatterns = patterns('',

    url( r'^', include( user_resource.urls ) ),
    url( r'^', include( researcher_resource.urls ) ),
    url( r'^', include( scientific_resource.urls ) ),
    url( r'^', include( position_resource.urls ) ),
    url( r'^', include( supplier_resource.urls ) ),

)
