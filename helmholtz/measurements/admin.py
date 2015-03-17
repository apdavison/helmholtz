#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.measurements.models import Parameter, Measurement

# overriding
class ParameterAdmin( GuardedModelAdmin ) :
    pass

class MeasurementAdmin( GuardedModelAdmin ) :
    pass

# registration
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Measurement, MeasurementAdmin)
