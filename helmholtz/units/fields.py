#encoding:utf-8
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.db import models
from itertools import chain
from django.core.exceptions import ValidationError
from django import forms

class PhysicalQuantity(object):
    """
    Python object returned when a :class:`PhysicalQuantityField`
    is accessed from an object.
    """
    
    def __init__(self, value, unit=None):
        self.value = float(value)
        self.unit = unit
    
    def __str__(self):
        if self.unit:
            return "%.2f %s" % (self.value, self.unit)
        else:
            return "%s" % self.value
    
    def db_repr(self):
        return """(%s,"%s")""" % (self.value, self.unit)
    
    def __unicode__(self):
        return u"%s" % self.__str__()
    
    def __repr__(self):
        return "PhysicalQuantity(%s,%s)" % (self.value, self.unit)
    
    def as_tuple(self):
        return (self.value, self.unit)

class PhysicalQuantityFormField(forms.CharField):
    """
    A subclass of :class:`CharField` creating a :class:`PhysicalQuantity`
    instance from the user inputs.
    """
    
    def to_python(self, value):
        if not value[0] :
            if not self.required :
                return None
            else :
                raise ValidationError('please specify parameter value')
        else :
            val = float(value[0])
            unit = value[1]
            return PhysicalQuantity(val, unit)    

class UnitWidget(forms.Select):
    """A subclass of :class:`Select` displaying a choice of :class:`Unit` instances."""
    
    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label):
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            return u'<option value="%s"%s>%s</option>' % (
                escape(option_value), selected_html,
                force_unicode(option_label).replace('&amp;', '&'))
        # Normalize to strings
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label))
        return u'\n'.join(output)

class PhysicalQuantityWidget(forms.MultiWidget):
    """
    A subclass of :class:`MultiWidget` that splits physical quantity input into two <input type="text"> boxes.
    """
    def __init__(self, attrs=None, initial_unit=None):
        self.initial_unit = initial_unit
        widgets = (forms.TextInput(attrs=attrs['left'] if attrs.has_key('left') else None),
                   forms.TextInput(attrs=attrs['right'] if attrs.has_key('right') else None))
        super(PhysicalQuantityWidget, self).__init__(widgets, attrs['all'] if attrs.has_key('all') else None)

    def value_from_datadict(self, data, files, name):
        values = super(PhysicalQuantityWidget, self).value_from_datadict(data, files, name)
        return values

    def decompress(self, value):
        if value:
            return [value.value, value.unit]
        return [None, self.initial_unit]

class PhysicalQuantityField(models.TextField):
    """
    A subclass of :class:`TextField` useful to
    store physical quantities in database.
    """
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, unit=None, *args, **kwargs):
        self.unit = unit
        super(PhysicalQuantityField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        # Passing max_length to forms.CharField means that the value's length
        # will be validated twice. This is considered acceptable since we want
        # the value in the form field (to pass into widget for example).
        widget = PhysicalQuantityWidget(attrs={'left':{'class':'form_sub_input_left'},
                                               'right':{'class':'form_sub_input_right'},
                                               'all':{}}, initial_unit=self.unit)
        defaults = {'widget':widget, 'required':not self.null}
        defaults.update(kwargs)
        return PhysicalQuantityFormField(**defaults)
    
    def db_prep_value(self, value):
        obj = PhysicalQuantity(value.value, self.unit) if ((not value.unit) and (self.unit)) else value
        return obj.db_repr() if obj else None
    
    def to_python(self, value):
        if isinstance(value, PhysicalQuantity) :
            return value
        if value :
            combination = [k for k in value.split(' ') if k != '']
            assert len(combination) in [1, 2], 'bad database field format'
            try:
                float_value = float(combination[0])
            except:
                raise Exception('bad database field format')
            unit = unicode(combination[1]) if len(combination) == 2 else None     
            return PhysicalQuantity(float_value, unit)
        else :
            return value
    
    def db_type(self, connection):
        dbtype = connection.creation.data_types['TextField']
        return dbtype 
    
    def get_prep_lookup(self, lookup_type, value):
        # We only handle 'exact' and 'in'. All others are errors.
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

class PhysicalQuantityArray(object):
    """
    Python object returned when a :class:`PhysicalQuantityArrayField`
    is accessed from an object.
    """
    def __init__(self, values, unit=None):
        self.values = [float(k) for k in values]
        self.unit = unit
    
    def db_repr(self):
        return """((%s),"%s")""" % (','.join([k for k in self.values]), self.unit)    
    
    def __str__(self):
        st = ','.join(["%.2f" % k for k in self.values])
        if self.unit :
            st += ' %s' % (self.unit) 
        return st
    
    def __unicode__(self):
        return u"%s" % self.__str__()
    
    def __repr__(self):
        return "PhysicalQuantityArray(%s,%s)" % (self.values, self.unit)
    
    def as_tuple(self):
        return (self.values, self.unit)

class PhysicalQuantityArrayField(models.TextField):
    """
    A subclass of :class:`TextField` useful to store a set
    of physical quantities having the same unit in database.
    """
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, unit=None, *args, **kwargs):
        self.unit = unit
        super(PhysicalQuantityArrayField, self).__init__(*args, **kwargs)
    
    def db_prep_value(self, value):
        obj = PhysicalQuantityArray(value.values, self.unit) if ((not value.unit) and (self.unit)) else value
        return obj.db_repr() if obj else None
    
    def to_python(self, ar):
        if isinstance(ar, PhysicalQuantityArray) :
            return ar
        if ar :
            combination = [k for k in ar.split(' ') if k != '']
            assert len(combination) in [1, 2], 'bad database field format'
            try:
                values = [float(k) for k in combination[0].split(',')]
            except:
                raise Exception('bad database field format')
            if len(combination) == 2 :
                unit = str(combination[1])
            else:
                unit = None   
            return PhysicalQuantityArray(values, unit)   
        else :
            return None
    
    def db_type(self, connection):
        dbtype = connection.creation.data_types['TextField']
        return dbtype
    
    def get_prep_lookup(self, lookup_type, value):
        # We only handle 'exact' and 'in'. All others are errors.
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

class ArrayOfPhysicalQuantity(object):
    """
    Python object returned when a :class:`ArrayOfPhysicalQuantityField`
    is accessed from an object.
    """
    def __init__(self, values):
        assert type(values) in [list, tuple], "values must be a list or tuple"
        assert len(values), "values must not be empty"
        for value in values :
            assert isinstance(value, PhysicalQuantity), "values must be PhysicalQuantities"
        self.values = values   
    
    def db_repr(self):
        st = '{'
        l = len(self.values)
        i = 1
        for value in self.values :
            st += """{'%s','%s'}""" % (value.value, value.unit)
            if i < l :
                st += ','    
            i += 1
        st += '}'
        return st 
    
    def __str__(self):
        return str(self.values)
    
    def __unicode__(self):
        return u"%s" % self.__str__()
    
    def __repr__(self):
        return "ArrayOfPhysicalQuantity(%s)" % (self.values)

class ArrayOfPhysicalQuantityField(models.Field):
    """
    A subclass of :class:`TextField` useful to store a set of physical
    quantities not necessarily having the same unit in database.
    """
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        super(ArrayOfPhysicalQuantityField, self).__init__(*args, **kwargs)
    
    def db_type(self, connection):
        return 'varchar[][2]'
    
    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        if lookup_type == 'isnull' :
            raise Exception('Not Implemented')
        elif lookup_type == 'exact':
            return super(ArrayOfPhysicalQuantityField, self).get_db_prep_lookup(lookup_type, value, connection, prepared=False)
        elif lookup_type == 'in':
            raise Exception('Not Implemented')
        else:
            raise TypeError('Lookup type %s is not supported.' % lookup_type)
    
    def get_prep_value(self, value):
        return value.db_repr() if value else None
    
    def to_python(self, value):
        if isinstance(value, ArrayOfPhysicalQuantity) :
            return value
        if value :   
            ar = list()
            for item in value :
                ph_quantity = PhysicalQuantity(item[0], item[1])    
                ar.append(ph_quantity)
            return ArrayOfPhysicalQuantity(ar)
        else :
            return value

class ArrayToStringField(models.TextField):
    """A convenient subclass of :class:`TextField` to store in a raw way array of data."""
    pass
