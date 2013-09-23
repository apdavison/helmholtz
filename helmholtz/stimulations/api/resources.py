# chemistry/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.stimulations.models import Type
from helmholtz.stimulations.models import Stimulus
from helmholtz.stimulations.models import Spike
from helmholtz.stimulations.models import DriftingGrating
from helmholtz.stimulations.models import Multi

# Allowed resources
from helmholtz.devices.api.resources import ItemResource


# Resources
class TypeResource( ModelResource ) :
    class Meta:
        queryset = Type.objects.all()
        resource_name = 'type'
        filtering = {
            'name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class StimulusResource( ModelResource ) :
    type = fields.ForeignKey( TypeResource, 'type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( ItemResource, 'stimulus_generator', null=True )
    class Meta:
        queryset = Stimulus.objects.all()
        resource_name = 'stimulus'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SpikeResource( ModelResource ) :
    type = fields.ForeignKey( TypeResource, 'type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( ItemResource, 'stimulus_generator', null=True )
    class Meta:
        queryset = Spike.objects.all()
        resource_name = 'spike'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class MultiResource( ModelResource ) :
    type = fields.ForeignKey( TypeResource, 'type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( ItemResource, 'stimulus_generator', null=True )

    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle

    class Meta:
        queryset = Multi.objects.all()
        resource_name = 'multi'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class DriftingGratingResource( ModelResource ) :
    type = fields.ForeignKey( TypeResource, 'type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( ItemResource, 'stimulus_generator', null=True )

    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle

    class Meta:
        queryset = DriftingGrating.objects.all()
        resource_name = 'driftinggrating'
        excludes = ['id']
        filtering = {
            'label': ('exact','startswith',),
            'type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
            'stimulation_shape': ALL,
            'contrast': ALL,
            'theta': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

