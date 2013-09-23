# species/api.py

from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from helmholtz.species.models import Species
from helmholtz.species.models import Strain


# Resources
class SpeciesResource( ModelResource ) :
    class Meta:
        queryset = Species.objects.all()
        resource_name = 'species' # optional, if not present it will be generated from classname
        #excludes = ['id']
        filtering = {
            'scientific_name': ALL,
            'english_name': ALL,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        always_return_data = True
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    #def create_response( self, request, bundle, response_class, **response_kwargs ):
    #    desired_format = self.determine_format( request )
    #    serialized = self.serialize( request, bundle, desired_format )
    #    response = response_class( content=serialized, content_type=build_content_type(desired_format), **response_kwargs )
    #    response['Content-Length'] = len( response.content )
    #    return response

class StrainResource( ModelResource ) :
    species = fields.ForeignKey( SpeciesResource, 'species' )

    class Meta:
        queryset = Strain.objects.all()
        resource_name = 'strain'
        excludes = ['id']
        filtering = {
            'nomenclature' : ALL,
            'label' : ALL,
            'species' : ALL_WITH_RELATIONS,
        }
        allowed_methods = [ 'get', 'post', 'put', 'delete', 'patch' ]
        always_return_data = True
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
