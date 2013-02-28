# chemistry/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.stimulation.models import StimulationType
from helmholtz.stimulation.models import Stimulus
from helmholtz.stimulation.models import SpikeStimulus
from helmholtz.stimulation.models import DriftingGratingStimulus
from helmholtz.stimulation.models import MultiStimulus

# Allowed resources
from helmholtz.device.api.resources import DeviceResource


# Resources
class StimulationTypeResource( ModelResource ) :
    class Meta:
        queryset = StimulationType.objects.all()
        resource_name = 'stimulationtype'
        filtering = {
            'name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class StimulusResource( ModelResource ) :
    stimulation_type = fields.ForeignKey( StimulationTypeResource, 'stimulation_type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( DeviceResource, 'stimulus_generator', null=True )
    class Meta:
        queryset = Stimulus.objects.all()
        resource_name = 'stimulus'
        filtering = {
            'label': ALL,
            'stimulation_type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class SpikeStimulusResource( ModelResource ) :
    stimulation_type = fields.ForeignKey( StimulationTypeResource, 'stimulation_type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( DeviceResource, 'stimulus_generator', null=True )
    class Meta:
        queryset = SpikeStimulus.objects.all()
        resource_name = 'spikestimulus'
        filtering = {
            'label': ALL,
            'stimulation_type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class MultiStimulusResource( ModelResource ) :
    stimulation_type = fields.ForeignKey( StimulationTypeResource, 'stimulation_type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( DeviceResource, 'stimulus_generator', null=True )

    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle

    class Meta:
        queryset = MultiStimulus.objects.all()
        resource_name = 'multistimulus'
        filtering = {
            'label': ALL,
            'stimulation_type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()



class DriftingGratingStimulusResource( ModelResource ) :
    stimulation_type = fields.ForeignKey( StimulationTypeResource, 'stimulation_type', null=True, full=True )
    stimulus_generator = fields.ForeignKey( DeviceResource, 'stimulus_generator', null=True )

    def dehydrate( self, bundle ):
        for key in bundle.data.keys() :
            if bundle.data[key] is None :
                bundle.data.pop( key )
        return bundle

    class Meta:
        queryset = DriftingGratingStimulus.objects.all()
        resource_name = 'driftinggratingstimulus'
        filtering = {
            'label': ALL,
            'stimulation_type': ALL_WITH_RELATIONS,
            'stimulus_generator': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

