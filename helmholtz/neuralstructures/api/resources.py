# neuralstructures/api/resources.py
from django.conf.urls import url

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.neuralstructures.models import BrainRegion
from helmholtz.neuralstructures.models import CellType
from helmholtz.neuralstructures.models import Cell

# Allowed resources
from helmholtz.species.api.resources import SpeciesResource


# Resources
class BrainRegionResource( ModelResource ) :
    parent = fields.ForeignKey( 'self', 'parent', null=True )
    species = fields.ToManyField( SpeciesResource, 'species' )
    class Meta:
        queryset = BrainRegion.objects.all()
        resource_name = 'brainregion' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'name': ALL,
            'parent': ALL_WITH_RELATIONS,
            'species': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class CellTypeResource( ModelResource ) :
    brain_regions = fields.ToManyField( BrainRegionResource, 'brain_regions' )
    class Meta:
        queryset = CellType.objects.all()
        resource_name = 'celltype'
        excludes = ['id']
        filtering = {
            'name': ALL,
            'brain_regions': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class CellResource( ModelResource ) :
    type = fields.ForeignKey( CellTypeResource, 'type' )
    class Meta:
        queryset = Cell.objects.all()
        resource_name = 'cell'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'type': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
