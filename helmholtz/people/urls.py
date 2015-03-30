from django.conf.urls import patterns, url, include

# tastypie resource exposition
from helmholtz.people.api.resources import UserResource
from helmholtz.people.api.resources import ResearcherResource
from helmholtz.people.api.resources import OrganizationResource
from helmholtz.people.api.resources import PositionResource
from helmholtz.people.api.resources import SupplierResource
# instance
user_resource = UserResource()
researcher_resource = ResearcherResource()
organization_resource = OrganizationResource()
position_resource = PositionResource()
supplier_resource = SupplierResource()

urlpatterns = patterns('',

    url( r'^', include( user_resource.urls ) ),
    url( r'^', include( researcher_resource.urls ) ),
    url( r'^', include( organization_resource.urls ) ),
    url( r'^', include( position_resource.urls ) ),
    url( r'^', include( supplier_resource.urls ) ),

)
