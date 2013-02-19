#encoding:utf-8
from django.db import models
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from helmholtz.experiment.models import Experiment
from helmholtz.device.models import DeviceProperties
from helmholtz.stimulation.models import Stimulus
from helmholtz.storage.models import File


class RecordingBlock( models.Model ) :
    """Split an :class:`Experiment` into several sequences of recording."""
    experiment = models.ForeignKey( Experiment )
    name = models.CharField( max_length=250, null=True, blank=True )
    description = models.TextField( null=True, blank=True )
    start = models.DateTimeField( null=True, blank=True )
    end = models.DateTimeField( null=True, blank=True )
    notes = models.TextField( null=True, blank=True )
    
    def __unicode__(self):
        st = "Recording block %s" % self.pk
        if self.name :
            st += " called '%s'" % self.name
        return st
    

class ProtocolRecording( models.Model ) :
    """
    Split a :class:`RecordingBlock` instance into several stimulation protocols.
    Equivalent to the Neo :class:`Block` 
    """
    block = models.ForeignKey( RecordingBlock )
    name = models.CharField( max_length=250 )
    file = models.ForeignKey( File, null=True, blank=True )
    rec_datetime = models.DateTimeField( null=True, blank=True )
    description = models.TextField( null=True, blank=True )
    is_continuous = models.NullBooleanField( null=True, blank=True )
    stimulus = models.ForeignKey( Stimulus, null=True, blank=True )
    
    def __unicode__(self):
        return "Procotol Recording '%s'" % (self.name)
    

class Segment( models.Model ) :
    """
    Groups one or more :class:`ContinuousSignal` or :class:`DiscreteSignal`
    Equivalent to the Neo :class:`Segment` 
    """
    recording = models.ForeignKey( ProtocolRecording )
    name = models.CharField( max_length=250 )
    description = models.TextField( null=True, blank=True )
    file = models.ForeignKey( File, null=True, blank=True )
    rec_datetime = models.DateTimeField( null=True, blank=True )
    
    def __unicode__(self):
        return "Segment '%s'" % (self.name)


class ContinuousSignal( models.Model ) :
    """
    Single dataset stored in a file.
    Equivalent to the Neo :class:`AnalogSignal` 
    """
    segment = models.ForeignKey( Segment )
    units = models.CharField( max_length=10 )
    sampling_rate = models.FloatField( )
    file = models.ForeignKey( File, null=True, blank=True )
    name = models.CharField( max_length=250 )
    description = models.TextField( null=True, blank=True )
    start = models.TimeField( null=True, blank=True )
    stop = models.TimeField( null=True, blank=True )
    #channel_index is in RecordingChannel
    
    def __unicode__(self):
        return "Continuous Signal '%s'" % (self.name)


class DiscreteSignal( models.Model ) :
    """
    Single dataset stored in a file.
    Equivalent to the Neo :class:`SpikeTrain` 
    """
    segment = models.ForeignKey( Segment )
    units = models.CharField( max_length=10 )
    sampling_rate = models.FloatField( )
    file = models.ForeignKey( File, null=True, blank=True )
    name = models.CharField( max_length=250 )
    description = models.TextField( null=True, blank=True )
    start = models.TimeField( null=True, blank=True )
    stop = models.TimeField( null=True, blank=True )
    #channel_index is in RecordingChannel
    waveform_description = models.TextField( null=True, blank=True )
    left_sweep = models.FloatField( null=True, blank=True )
    
    def __unicode__(self):
        return "Discrete Signal '%s'" % (self.name)


class RecordingChannel( models.Model ) :
    """Store channels used by the ProtocolRecording instance to make acquisition."""
    protocol = models.ForeignKey( ProtocolRecording ) # like in neo, it depends on Block as Segment
    index = models.IntegerField( default=0 )
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField( null=True, blank=True )
    file = models.ForeignKey( File, null=True, blank=True )
    continuous_signals = models.ManyToManyField( ContinuousSignal, null=True )
    configuration = models.ForeignKey( DeviceProperties, null=True )

    def __unicode__(self):
        return "Recording Channel '%s'" % (self.name)
