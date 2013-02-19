#encoding:utf-8
import re
from django.core.exceptions import ValidationError
from django.db.models.base import ModelBase
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from helmholtz.core.models import Cast
from helmholtz.units.models import Unit

def is_range(value):
    regexp = "^(\[|\])\-{0,1}\d+(\.\d+){0,1}:\-{0,1}\d+(\.\d+){0,1}:\-{0,1}\d+(\.\d+){0,1}(\]|\[)$"
    match = re.match(regexp, value, re.UNICODE)
    if match :
        return True
    else :
        return False

def get_start_end_step(range):
    "Return start, end and step of the specified range"
    interval = range[1:-1].split(':')
    return interval[0], interval[2], interval[1]

def get_evaluations(start, end, step, tp=float):
    return tp(start), tp(end), tp(step)

def verify_pattern(pattern):
    """Verify if the specified pattern is correctly defined."""
    regexp = "^(((\[|\])\-{0,1}\d+(\.\d+){0,1}:\-{0,1}\d+(\.\d+){0,1}:\-{0,1}\d+(\.\d+){0,1}(\[|\]))|\w+|\w+(\.\w+)|(\-{0,1}\d+(\.\d+)))((\|(((\[|\])\-{0,1}\d+(\.\d+){0,1}:\-{0,1}\d+(\.\d+){0,1}:\-{0,1}\d+(\.\d+){0,1}(\[|\]))|\w+|(\-{0,1}\d+(\.\d+))))*)$"
    match = re.match(regexp, pattern, re.UNICODE)
    if not match :
        raise ValidationError("bad pattern format")   
    else :
        n = 1
        for single_pattern in pattern.split('|') :
            if is_range(single_pattern) :
                start, end, step = get_start_end_step(single_pattern)
                f_start, f_end, f_step = get_evaluations(start, end, step)
                #as pattern is a range, step cannot be zero
                if not (f_step < 0 or f_step > 0) :
                    raise ValidationError("bad range format, step value of pattern number %s cannot be zero" % n) 
                #verify that lower and upper bound are coherent with the specified step
                if ((f_step >= 0) and (f_start > f_end)) or ((f_step < 0) and (f_end > f_start)) :
                    raise ValidationError("bad range format, pattern number %s would be [%s:%s:%s]" % (n, end, step, start))
                n += 1
                    


choices = (('I', 'integer'), ('F', 'float'), ('S', 'string'), ('B', 'boolean'))
class Parameter(models.Model):
    """Extend base properties of a class."""
    label = models.CharField(max_length=50)
    verbose_name = models.TextField(null=True, blank=True)
    pattern = models.TextField(null=True, blank=True, help_text="constraints a measure to a set of values defined like this : [first1:step1:last1]|[first2:step2:last2] or text1|text2|text3")
    type = models.CharField(max_length=1, choices=choices)
    unit = models.ForeignKey(Unit, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    def get_type(self):
        """Get the Python type corresponding to the Parameter type."""
        dct = {
            'I':int,
            'F':float,
            'S':unicode,
            'B':bool,
            'M':ModelBase
        }
        return dct[self.type]

    def __unicode__(self):
        return self.label



class Measurement( models.Model ):
    """
    Base class of all kind of measurements. Subclasses set the value and unit 
    of additional parameters defined into the Parameter class.
    """
    parameter = models.ForeignKey( Parameter )
    unit = models.ForeignKey( Unit, null=True, blank=True )
    timestamp = models.DateTimeField( null=True, blank=True )
    # generic link
    content_type = models.ForeignKey( ContentType, null=True, blank=True )
    object_id = models.PositiveIntegerField( null=True, blank=True )
    object = generic.GenericForeignKey( 'content_type', 'object_id' )
    # value stored
    bool_value = models.BooleanField( default=False )
    integer_value = models.IntegerField( null=True, blank=True )
    float_value = models.FloatField( null=True, blank=True )
    string_value = models.TextField( null=True, blank=True )
    
    def get_unit(self):
        return self.unit if self.unit else (self.parameter.unit if self.parameter.unit else None)
    
    def get_symbol(self):
        return self.get_unit().symbol if self.unit else None
    symbol = property(get_symbol)        
    
    def __unicode__(self):
        value = 0
        if self.parameter.type == 'I' :
            value = self.integer_value
        elif self.parameter.type == 'F' :
            value = self.float_value
        elif self.parameter.type == 'S' :
            value = self.string_value
        elif self.parameter.type == 'B' :
            value = self.boolean_value
        return "%s(%s):%s %s at %s on object %s" % (self.parameter.label, self.parameter.type, value, self.unit, self.timestamp, self.object)


