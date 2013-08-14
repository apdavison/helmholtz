# simple odml serializer
    
try:
    import defusedxml.lxml as lxml
    from lxml.etree import Element, SubElement, tostring
except ImportError:
    lxml = None

import re

from django.utils import six
from django.utils.encoding import force_unicode

from tastypie.bundle import Bundle

from tastypie.serializers import Serializer


class HelmholtzSerializer( Serializer ):

    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'odml']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'odml': 'text/odml',
    }

    def to_odml( self, data, options=None ):
        options = options or {}
        if lxml is None:
            raise ImproperlyConfigured("Usage of the odML apects requires lxml and defusedxml.")
        return tostring( self.odml_tree( data, options, name=None, depth=0 ), xml_declaration=True, encoding='utf-8' )

    def odml_tree( self, data, options=None, name=None, depth=0 ):
        # List
        if isinstance(data, (list, tuple)):
            element = Element(name or 'objects')
            if name:
                element = Element(name) # TODO: here are the list of objects!!!!
                element.set('type', 'list')
            else:
                element = Element('objects')
                #element = Element('list')
            for item in data:
                element.append(self.odml_tree(item, options, depth=depth+1))
                element[:] = sorted(element, key=lambda x: x.tag)
        # Dictionary
        elif isinstance(data, dict):
            if depth == 0:
                element = Element('odML')
            else:
                element = Element(name or 'response')
                element.set('type', 'hash')
            for (key, value) in data.items():
                element.append( self.odml_tree(value, options, name=key, depth=depth+1) )
                element[:] = sorted(element, key=lambda x: x.tag)
        # Object
        elif isinstance(data, Bundle):
            element = Element('section')
            # attributes
            #if data.related_name is None:
            if data.request is None:
                element.set( 'name', 'undefined' )
                #element.set( 'depth', str(depth) )
            else:
                element.set( 'name', re.sub( "^/|/[0-9]*$", "", data.request.path ) )
            # odml type
            odml_type = SubElement( element, 'type' )
            odml_type.text = 'undefined'
            # odml repository
            odml_repo = SubElement( element, 'repository' )
            odml_repo.text = 'http://www.g-node.org/odml/terminologies/v1.0/terminologies.xml'
            # subobjects
            for field_name, field_object in data.data.items():
                prop = SubElement( element, 'property' )
                # name
                prop_name = SubElement( prop, 'name' )
                prop_name.text = field_name
                # type
                prop_type = SubElement( prop, 'type' )
                prop_type.text = get_type_string(field_object)
                # value
                prop_value = SubElement( prop, 'value' )
                prop_value.text = field_object
            # after processing, if is a single section
            # wrap it with a an odML container
            if depth == 0:
                root = Element('odML')
                root.append( element )
                element = root
        # Expansion
        elif hasattr(data, 'dehydrated_type'):
            if getattr(data, 'dehydrated_type', None) == 'related' and data.is_m2m == False:
                if data.full:
                    return self.odml_tree(data.fk_resource, options, name, depth+1)
                else:
                    return self.odml_tree(data.value, options, name, depth+1)
            elif getattr(data, 'dehydrated_type', None) == 'related' and data.is_m2m == True:
                if data.full:
                    element = Element(name or 'objects')
                    for bundle in data.m2m_bundles:
                        element.append(self.odml_tree(bundle, options, bundle.resource_name, depth+1))
                else:
                    element = Element(name or 'objects')
                    for value in data.value:
                        element.append(self.odml_tree(value, options, name, depth=depth+1))
            else:
                return self.odml_tree(data.value, options, name)
        # Value
        else:
            element = Element(name or 'value')
            simple_data = self.to_simple(data, options)
            data_type = get_type_string(simple_data)

            if data_type != 'string':
                element.set('type', get_type_string(simple_data))

            if data_type != 'null':
                if isinstance(simple_data, six.text_type):
                    element.text = simple_data
                else:
                    element.text = force_unicode(simple_data)
        # result
        return element

    def from_odml( self, content ):
        pass


# additional functions:
def get_type_string(data):
    """
    Translates a Python data type into a string format.
    """
    data_type = type(data)

    if data_type in six.integer_types:
        return 'integer'
    elif data_type == float:
        return 'float'
    elif data_type == bool:
        return 'boolean'
    elif data_type in (list, tuple):
        return 'list'
    elif data_type == dict:
        return 'hash'
    elif data is None:
        return 'null'
    elif isinstance(data, six.string_types):
        return 'string'
