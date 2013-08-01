#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.people.models import Organization
from helmholtz.people.models import Position
from helmholtz.people.models import Researcher
from helmholtz.people.models import Supplier

# overriding
class ResearcherAdmin( GuardedModelAdmin ) :
    fields = [
        'user',
        'phone',
        'website',
        'street_address',
        'postal_code',
        'town',
        'state',
        'country',
        'notes'
    ]

# registration
admin.site.register( Organization )
admin.site.register( Position )
admin.site.register( Researcher, ResearcherAdmin )
admin.site.register( Supplier )
