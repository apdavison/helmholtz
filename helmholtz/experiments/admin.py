#encoding:utf-8

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from helmholtz.experiments.models import Experiment

# overriding
class ExperimentAdmin( GuardedModelAdmin ) :
    fields = [
        'label',
        'type',
        'start',
        'end',
        'notes',
        'setup',
        'researchers',
        'preparation'
    ]

# registration
admin.site.register( Experiment, ExperimentAdmin )
