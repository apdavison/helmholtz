#encoding:utf-8
from django.db import models

from helmholtz.core.models import Cast
from helmholtz.device.models import Device
from helmholtz.units.fields import PhysicalQuantity
from helmholtz.units.fields import PhysicalQuantityField
#from helmholtz.units.fields import PhysicalQuantityArrayField
#from helmholtz.units.fields import ArrayToStringField


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
    start = PhysicalQuantityField(unit='ms', null=True, blank=True)
    duration = PhysicalQuantityField(unit='ms', null=True, blank=True)
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


multistim_types = (('SN', 'sparse noise'),('BDN', 'binary dense noise'), ('TDN', 'ternary dense noise'), ('SNN', 'sparse noise nrev'),('RC', 'revcor'),('RCO', 'revcor old'))

class MultiStimulus( Stimulus ) :
    title = models.CharField(max_length=32, null=True, blank=True)
    center_type = models.CharField(max_length=3, choices=multistim_types, null=True, blank=True)    
    nb_of_sequence = models.PositiveSmallIntegerField(null=True, blank=True)
    stimulus_duration = PhysicalQuantityField(unit='s', null=True, blank=True)
    pretrigger_duration = PhysicalQuantityField(unit='s', null=True, blank=True)
    acq_extra_time = PhysicalQuantityField(unit='s', null=True, blank=True)
    # receptive field
    rf_x = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_y = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_l = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_w = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_t = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    n_div_x = models.IntegerField(null=True, blank=True)
    n_div_y = models.IntegerField(null=True, blank=True)
    expansion = PhysicalQuantityField(unit='%', null=True, blank=True)
    scotoma = PhysicalQuantityField(unit='%', null=True, blank=True)
    initial_seed = models.IntegerField(null=True, blank=True)
    seed_constant = models.NullBooleanField(null=True, blank=True)
    luminance_high = PhysicalQuantityField(unit='Cd/m&sup2;', null=True, blank=True)
    luminance_background = PhysicalQuantityField(unit='Cd/m&sup2;', null=True, blank=True)
    luminance_low = PhysicalQuantityField(unit='Cd/m&sup2;', null=True, blank=True)
    nb_of_luminance = models.IntegerField(null=True, blank=True)
    nb_of_dton = models.IntegerField(null=True, blank=True)    
    dt_on_1 = PhysicalQuantityField(unit='s', null=True, blank=True)
    dt_on_2 = PhysicalQuantityField(unit='s', null=True, blank=True)
    dt_on_3 = PhysicalQuantityField(unit='s', null=True, blank=True)
    dt_off = PhysicalQuantityField(unit='s', null=True, blank=True)
    nb_of_object = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'multistim'
        verbose_name_plural = 'multistim stimuli'

    @property
    def stim_type(self):
        return self.get_type_display()

    def dt_on_str(self):
        st = ''
        if self.dt_on :
            st += ','.join(["%.2f" % k for k in self.dt_on.values if k])
            if self.dt_on.unit :
                st += ' %s' % (self.dt_on.unit) 
        return st



grating_type = (('Grating','Grating'), ('Gabor','Gabor'))
grating_shape = (('Rectangle','Rectangle'),('Circle','Circle'),('Ellipse','Ellipse'))
mvt_stim = (('Drifting','Drifting'), ('Phase-Antiphase','Phase-Antiphase'), ('On-Off','On-Off'), ('4 Directions','4 Directions'), ('Back-Forth','Back-Forth'))
class DriftingGratingStimulus( Stimulus ):
    title = models.CharField(max_length=32, null=True, blank=True)
    stim_type = models.CharField(max_length=7,choices=grating_type,null=True,blank=True)
    stim_shape = models.CharField(max_length=7,choices=grating_shape,null=True,blank=True)
    # receptive field
    rf_x = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_y = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_l = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_w = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    rf_t = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    position_x = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    position_y = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    length_x = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    length_y = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    theta = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    contrast = PhysicalQuantityField(unit='%', null=True, blank=True)
    phase = PhysicalQuantityField(unit='&deg;', null=True, blank=True)
    orientation = PhysicalQuantityField(unit='&deg;', null=True, blank=True) # how to map num_orientations
    num_orientations = models.IntegerField( default=0, null=True, blank=True )
    spatial_period = PhysicalQuantityField(unit='cycle/&deg;', null=True, blank=True) # 1/spatial_frequency
    phase_speed = PhysicalQuantityField(unit='&deg;/s', null=True, blank=True) # temporal_frequency ?
    mvt_stimulus = models.CharField(max_length=16,choices=mvt_stim,null=True,blank=True)
    nb_of_cycles = models.PositiveIntegerField(null=True, blank=True) # num_trials
    dt_on = PhysicalQuantityField(unit='ms',null=True,blank=True) # grating_duration
    dt_off = PhysicalQuantityField(unit='ms',null=True,blank=True) # grating_duration
    post_stim_time = PhysicalQuantityField(unit='ms', null=True, blank=True)
    block_stim = models.NullBooleanField(null=True,blank=True)
    random_blockstim = models.NullBooleanField(null=True,blank=True)
    sf_active = models.NullBooleanField(null=True,blank=True)
    sf_nb_stim = models.IntegerField(null=True, blank=True)
    sf_min = PhysicalQuantityField(unit='cycle/&deg;',null=True,blank=True)
    sf_max = PhysicalQuantityField(unit='cycle/&deg;',null=True,blank=True)
    tf_active = models.NullBooleanField(null=True,blank=True)
    tf_nb_stim = models.IntegerField(null=True, blank=True)
    tf_min = PhysicalQuantityField(unit='Hz',null=True,blank=True)
    tf_max = PhysicalQuantityField(unit='Hz',null=True,blank=True)
    spd_active = models.NullBooleanField(null=True,blank=True)
    spd_nb_stim = models.IntegerField(null=True, blank=True)
    spd_min = PhysicalQuantityField(unit='&deg;/s',null=True,blank=True)
    spd_max = PhysicalQuantityField(unit='&deg;/s',null=True,blank=True)
    ctr_active = models.NullBooleanField(null=True,blank=True)
    ctr_nb_stim = models.IntegerField(null=True, blank=True)
    ctr_min = PhysicalQuantityField(unit='%',null=True,blank=True)
    ctr_max = PhysicalQuantityField(unit='%',null=True,blank=True)
    phase_active = models.NullBooleanField(null=True,blank=True)
    phase_nb_stim = models.IntegerField(null=True, blank=True)
    phase_min = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    phase_max = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    ori_active = models.NullBooleanField(null=True,blank=True)
    ori_nb_stim = models.IntegerField(null=True, blank=True)
    ori_min = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    ori_max = PhysicalQuantityField(unit='&deg;',null=True,blank=True)
    pos_active = models.NullBooleanField(null=True,blank=True)
    pos_nb_x = models.IntegerField(null=True, blank=True)
    pos_nb_y = models.IntegerField(null=True, blank=True)
    size_active = models.NullBooleanField(null=True,blank=True)
    size_nb_stim = models.IntegerField(null=True, blank=True)
    size_min = PhysicalQuantityField(unit='%',null=True,blank=True)
    size_max = PhysicalQuantityField(unit='%',null=True,blank=True)
    do_blank = models.NullBooleanField(null=True,blank=True)
