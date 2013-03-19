#encoding:utf-8

from django.contrib import admin

from helmholtz.people.models import Organization
from helmholtz.people.models import Position
from helmholtz.people.models import Researcher
from helmholtz.people.models import Supplier

# registration
admin.site.register( Organization )
admin.site.register( Position )
admin.site.register( Researcher )
admin.site.register( Supplier )
