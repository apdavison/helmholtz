# chemistry/api/resources.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.drugs.models import RouteOfApplication
from helmholtz.drugs.models import DrugApplication
from helmholtz.drugs.models import ContinuousDrugApplication
from helmholtz.drugs.models import DiscreteDrugApplication

# Allowed resources
from helmholtz.experiments.api.resources import ExperimentResource
from helmholtz.chemistry.api.resources import SolutionResource


# Resources
class RouteOfApplicationResource( ModelResource ) :
    class Meta:
        queryset = RouteOfApplication.objects.all()
        resource_name = 'routeofapplication' # optional, if not present it will be generated from classname
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class DrugApplicationResource( ModelResource ) :
    experiment = fields.ForeignKey( ExperimentResource, 'experiment' )
    solution = fields.ForeignKey( SolutionResource, 'solution' )
    class Meta:
        queryset = DrugApplication.objects.all()
        resource_name = 'drugapplication'
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class ContinuousDrugApplicationResource( DrugApplicationResource ) :
    class Meta:
        queryset = ContinuousDrugApplication.objects.all()
        resource_name = 'continuousdrugapplication'


class DiscreteDrugApplicationResource( DrugApplicationResource ) :
    class Meta:
        queryset = DiscreteDrugApplication.objects.all()
        resource_name = 'discretedrugapplication'
