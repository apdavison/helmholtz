# species/api.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL
from tastypie import fields

from helmholtz.units.models import Unit


# Resources
class UnitResource( ModelResource ) :
    class Meta:
        queryset = Unit.objects.all()
        resource_name = 'unit' # optional, if not present it will be generated from classname
        filtering = {
            'symbol': ALL,
            'physical_meaning': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
