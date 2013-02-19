# chemistry/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.preparation.models import Animal
from helmholtz.preparation.models import Preparation

# Allowed resources
from helmholtz.species.api.resources import StrainResource
from helmholtz.device.api.resources import DeviceResource
from helmholtz.measurements.api.resources import MeasurementResource
from helmholtz.chemistry.api.resources import SolutionResource
from helmholtz.people.api.resources import SupplierResource


# Resources
class AnimalResource( ModelResource ) :
    strain = fields.ForeignKey( StrainResource, 'strain' )
    supplier = fields.ForeignKey( SupplierResource, 'supplier' )
    class Meta:
        queryset = Animal.objects.all()
        resource_name = 'animal'
        filtering = {
            'identifier': ALL,
            'nickname': ALL,
            'strain': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class PreparationResource( ModelResource ) :
    animal = fields.ForeignKey( AnimalResource, 'animal' )
    device = fields.ForeignKey( DeviceResource, 'device', null=True )
    cutting_solution = fields.ForeignKey( SolutionResource, 'cutting_solution', null=True )
    bath_solution = fields.ForeignKey( SolutionResource, 'bath_solution', null=True )
    class Meta:
        queryset = Preparation.objects.all()
        resource_name = 'preparation'
        filtering = {
            'type': ALL,
            'protocol': ALL,
            'animal': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

