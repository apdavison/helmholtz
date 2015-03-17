# measurements/api/resources.py

import json
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.conf.urls import url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
# special url treatment
from tastypie.http import HttpBadRequest
from tastypie.http import HttpForbidden
from tastypie.http import HttpCreated


from helmholtz.measurements.models import Parameter
from helmholtz.measurements.models import Measurement

from helmholtz.units.api.resources import UnitResource

# Allowed resources for measurement
from helmholtz.neuralstructures.models import Cell
from helmholtz.neuralstructures.api.resources import CellResource
from helmholtz.preparations.models import Animal
from helmholtz.preparations.models import Preparation
from helmholtz.preparations.api.resources import AnimalResource
from helmholtz.preparations.api.resources import PreparationResource
from helmholtz.devices.models import Item
from helmholtz.devices.api.resources import ItemResource


# Resources
class ParameterResource( ModelResource ) :
    unit = fields.ForeignKey( UnitResource, 'unit' )
    class Meta:
        queryset = Parameter.objects.all()
        resource_name = 'parameter' # optional, if not present it will be generated from classname
        excludes = ['id']
        filtering = {
            'label': ALL,
            'pattern': ALL,
            'type': ALL,
            'unit': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class MeasurementResource( ModelResource ) :
    parameter = fields.ForeignKey( ParameterResource, 'parameter' )
    unit = fields.ForeignKey( UnitResource, 'unit' )
    object = GenericForeignKeyField( {
        Cell: CellResource,
        Animal: AnimalResource,
        Item: ItemResource,
        Preparation: PreparationResource,
    }, 'object' ) # add the others here

    class Meta:
        queryset = Measurement.objects.all()
        resource_name = 'measurement'
        excludes = ['id']
        filtering = {
            'parameter' : ALL_WITH_RELATIONS,
            'unit' : ALL_WITH_RELATIONS,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]


# To be able to set measurement onto several models
# in root project/urls.py an url on top of the others catches all .../resource_name/pk/measurement/ posts
# and applies this view:

@csrf_exempt
def set_measurement_by_name( request, resource_name, pk ) :
    resource_app = resource_name +'s'
    return set_measurement( request, resource_app, resource_name, pk )

@csrf_exempt
def set_measurement( request, resource_app, resource_name, pk ) :
    mr = MeasurementResource()
    mr.method_check( request, allowed=['post'] )
    mr.is_authenticated( request )
    # get POST-ed data
    data = json.loads( request.raw_post_data )
    # check POST-ed data
    response = HttpBadRequest
    if not 'parameter' in data :
        return mr.create_response( request, None, response_class=response )
    if not 'value' in data :
        return mr.create_response( request, None, response_class=response )
    # get parameter by label
    p = Parameter.objects.filter( label=data['parameter'] )[0]
    if not p :
        response = HttpBadRequest
        return mr.create_response( request, None, response_class=response )
    else :
        # get the content_type id for the current resource_name
        ctype = ContentType.objects.get( model=resource_name )
        # set the measurements for the current resource object
        if p.type == 'F':
            m = Measurement( parameter=p, unit=p.unit, timestamp=datetime.now(), content_type=ctype, object_id=int(pk), float_value=data['value'] )
        elif p.type == 'I':
            m = Measurement( parameter=p, unit=p.unit, timestamp=datetime.now(), content_type=ctype, object_id=int(pk), integer_value=data['value'] )
        elif p.type == 'S':
            m = Measurement( parameter=p, unit=p.unit, timestamp=datetime.now(), content_type=ctype, object_id=int(pk), string_value=data['value'] )
        elif p.type == 'B':
            m = Measurement( parameter=p, unit=p.unit, timestamp=datetime.now(), content_type=ctype, object_id=int(pk), bool_value=data['value'] )
        m.save()
        response = HttpCreated
    # prepare response
    return mr.create_response( request, [], response_class=response )
    
