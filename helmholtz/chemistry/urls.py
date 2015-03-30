from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

# tastypie resource exposition
from helmholtz.chemistry.api.resources import SubstanceResource
from helmholtz.chemistry.api.resources import ProductResource
from helmholtz.chemistry.api.resources import SolutionResource
from helmholtz.chemistry.api.resources import QuantityOfSubstanceResource
# instance
Substance_resource = SubstanceResource()
Product_resource = ProductResource()
Solution_resource = SolutionResource()
QuantityOfSubstance_resource = QuantityOfSubstanceResource()

urlpatterns = patterns('',

    url( r'^', include( Substance_resource.urls ) ),
    url( r'^', include( Product_resource.urls ) ),
    url( r'^', include( Solution_resource.urls ) ),
    url( r'^', include( QuantityOfSubstance_resource.urls ) ),

)
