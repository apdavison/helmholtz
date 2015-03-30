# experiments/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.core.api.authorization import GuardianAuthorization

from helmholtz.experiments.models import Experiment

# Allowed resources
from helmholtz.people.api.resources import ResearcherResource
from helmholtz.devices.api.resources import SetupResource
from helmholtz.preparations.api.resources import PreparationResource

# Resources
class ExperimentResource(ModelResource) :
    setup = fields.ForeignKey(SetupResource, 'setup')
    researchers = fields.ToManyField(ResearcherResource, 'researchers')
    preparation = fields.ForeignKey(PreparationResource, 'preparation', null=True)
    blocks = fields.ToManyField('helmholtz.recordings.api.resources.BlockResource', 'block_set', null=True)
    class Meta:
        queryset = Experiment.objects.all()
        resource_name = 'experiment'
        excludes = ['id']
        filtering = {
            'label': ALL,
            'type': ALL,
            'start': ALL,
            'end': ALL,
            'researchers': ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()
        authorization = GuardianAuthorization()
