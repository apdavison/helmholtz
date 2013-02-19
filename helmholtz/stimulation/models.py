#encoding:utf-8
from django.db import models

from helmholtz.core.models import Cast
from helmholtz.device.models import Device


class StimulationType( models.Model ) :
    """Stimulation Type"""
    name = models.CharField( max_length=100, primary_key=True )

    def __unicode__(self):
       return self.name


class Stimulus( Cast ) :
    """
    Stimulation presented to/performed on a subject during an Experiment.
    Base class to derive actual stimulations from.
    """ 
    label = models.CharField( max_length=250, null=True, blank=True )
    stimulation_type = models.ForeignKey( StimulationType, null=True, blank=True )
    stimulus_generator = models.ForeignKey( Device, null=True, blank=True )
    start = models.FloatField( default=0.0, null=True, blank=True )
    duration = models.FloatField( default=0.0, null=True, blank=True )
    notes = models.CharField( max_length=250, null=True, blank=True )
    
    def __unicode__(self):
        st = '%s:%s' % (self.__class__.__name__, self.pk)
        if self.label :
            st += " called '%s'" % self.label
        if self.stimulation_type :
            st += ", type:'%s'" % self.stimulation_type.name
        return st
    
    class Meta:
        verbose_name_plural = 'stimuli'


# DERIVED STIMULI
class SpikeStimulus( Stimulus ) :
    """
    Stimulus made of spike, to be used by simulations.
    """
    class Meta:
        verbose_name_plural = 'Spike stimuli'
