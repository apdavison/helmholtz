#encoding:utf-8
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

#from helmholtz.neuralstructures import CellType
#from helmholtz.neuralstructures import Cell
#from helmholtz.stimulation import Stimulus


class DataSource( models.Model ):
    """
    Class of all kind of data sources for analysis purposes.
    """
    # link to actual data
    content_type = models.ForeignKey( ContentType, null=True, blank=True )
    object_id = models.PositiveIntegerField( null=True, blank=True )
    object = generic.GenericForeignKey( 'content_type', 'object_id' )
    # general info
    #cell_type = models.ForeignKey( CellType, null=True, blank=True )
    #cell = models.ForeignKey( Cell, null=True, blank=True )
    #stimulus = models.ForeignKey( Stimulus, null=True, blank=True )
    
    def __unicode__(self):
        return "DataSource: object %s (%s)" % ( self.object, self.content_type )


class Step( models.Model ):
    inputs = models.ManyToManyField( DataSource, related_name='inputs', null=True, blank=True )
    outputs = models.ManyToManyField( DataSource, related_name='outputs' )
    algorithm = models.CharField( max_length=100 )
    parameters = models.CharField( max_length=250, null=True, blank=True )
    
    def __unicode__(self):
        st = "%s producing %s" % ( self.algorithm, self.outputs )
        if self.inputs :
            st += " applied on $s" % ( self.input )
        return st
