#encoding:utf-8
from django.db import models

from helmholtz.units.models import Unit
from helmholtz.chemistry.models import Solution
from helmholtz.experiments.models import Experiment


class RouteOfApplication( models.Model ):
    """
    Store the route of application used by a :class:`DrugApplication` :
    
    ``name`` : the identifier of the route of application.
    """
    name = models.CharField(max_length=15, primary_key=True)
    
    def __unicode__(self):
        return self.name


roles = (
    ( 'AE', 'anaesthetic' ),
    ( 'PL', 'paralytic' )
)
routes = (
    ( 'IV', 'intravenous' ),
    ( 'PF', 'perfusion' )
)
class DrugApplication( models.Model ):
    """
    Store drug applications that could be done on a
    :class:`Preparation` during an :class:`Experiment` :
    
    ``experiment`` : the experiment during which the drug application is done.
    
    ``solution`` : the solution used by the drug application.
    
    ``role`` : the effect of the drug application.
    
    ``route`` : the route of application of the drug application.
    
    ``notes`` : notes concerning the drug application.
    """
    experiment = models.ForeignKey(Experiment)
    solution = models.ForeignKey(Solution)
    role = models.CharField( max_length=2, choices=roles, null=True, blank=True)
    route = models.CharField( max_length=2, choices=routes, null=True, blank=True )
    unit = models.ForeignKey( Unit, null=True, blank=True, help_text="Units of the application rate or volume")
    notes = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self._meta.verbose_name + ' ' + str(self.id) + ' - ' + str(self.solution)

    def __str__(self):
        return self.__unicode__()


class ContinuousDrugApplication( DrugApplication ):
    """
    Store drug applications applied during a certain amount
    of time during an :class:`Experiment` on a :class:`Preparation` :
    
    ``start`` : start timestamp of the drug application.
    
    ``end`` : end timestamp of the drug application.
    
    ``rate`` : the rate of the drug application
    """
    start = models.DateTimeField(null=True, blank=True) 
    end = models.DateTimeField(null=True, blank=True) 
    rate = models.FloatField( null=True, blank=True)
     
    def get_duration(self) :
        if self.start and self.end:
            return self.end - self.start
        else:
            return None
    
    class Meta :
        ordering = ['-start']


class DiscreteDrugApplication( DrugApplication ):
    """
    Store drug applications applied at a precise moment
    of an :class:`Experiment` on a :class:`Preparation` :
    
    ``time`` : time of the drug application.
    
    ``volume`` : volume of the drug application
    """
    volume = models.FloatField( null=True, blank=True)
    time = models.DateTimeField( null=True, blank=True )
    
    class Meta :
        ordering = ['-time']
