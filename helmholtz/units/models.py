#encoding:utf-8
from django.db import models

class Unit( models.Model ) :
    """Store the unit corresponding to a physical quantity."""
    symbol = models.CharField( max_length=16 )
    physical_meaning = models.TextField()
    
    def __unicode__(self):
        return self.symbol

    def __str__(self):
        return self.__unicode__()