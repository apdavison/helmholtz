from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url

# tastypie resource exposition
from helmholtz.drugs.api.resources import RouteOfApplicationResource
from helmholtz.drugs.api.resources import DrugApplicationResource
from helmholtz.drugs.api.resources import ContinuousDrugApplicationResource
from helmholtz.drugs.api.resources import DiscreteDrugApplicationResource
# instance
RouteOfApplication_resource = RouteOfApplicationResource()
DrugApplication_resource = DrugApplicationResource()
ContinuousDrugApplication_resource = ContinuousDrugApplicationResource()
DiscreteDrugApplication_resource = DiscreteDrugApplicationResource()

urlpatterns = patterns('',

    url( r'^', include( RouteOfApplication_resource.urls ) ),
    url( r'^', include( DrugApplication_resource.urls ) ),
    url( r'^', include( ContinuousDrugApplication_resource.urls ) ),
    url( r'^', include( DiscreteDrugApplication_resource.urls ) ),

)
