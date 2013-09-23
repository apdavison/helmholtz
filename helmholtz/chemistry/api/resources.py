# chemistry/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.chemistry.models import Substance
from helmholtz.chemistry.models import Product
from helmholtz.chemistry.models import Solution
from helmholtz.chemistry.models import QuantityOfSubstance

# Allowed resources
from helmholtz.people.api.resources import SupplierResource


# Resources
class SubstanceResource( ModelResource ) :
    class Meta:
        queryset = Substance.objects.all()
        resource_name = 'substance' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class ProductResource( ModelResource ) :
    substance = fields.ForeignKey( SubstanceResource, 'substance' )
    supplier = fields.ForeignKey( SupplierResource, 'supplier' )
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'
        excludes = ['id']
        filtering = {
            'catalog_ref': ALL,
            'name': ALL,
            'substance': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SolutionResource( ModelResource ) :
    class Meta:
        queryset = Solution.objects.all()
        resource_name = 'solution'
        excludes = ['id']
        filtering = {
            'label': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class QuantityOfSubstanceResource( ModelResource ) :
    solution = fields.ForeignKey( SolutionResource, 'solution' )
    product = fields.ForeignKey( ProductResource, 'supplier' )
    class Meta:
        queryset = QuantityOfSubstance.objects.all()
        resource_name = 'quantityofsubstance'
        excludes = ['id']
        filtering = {
            'concentration': ALL,
            'solution': ALL_WITH_RELATIONS,
            'product': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
