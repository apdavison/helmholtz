#encoding:utf-8
from django.utils.datastructures import SortedDict
from django.db import models

from helmholtz.core.shortcuts import find_file

class CommunicationProtocol(models.Model):
    """Existing communication protocols."""
    name = models.TextField(primary_key=True)
    initials = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.initials

class MimeType(models.Model):
    """Existing type of :class:`File`."""
    extension = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.name
    shortname = property(__unicode__)

class FileServer(models.Model):
    """Physical storage where a :class:`File` could be stored."""
    label = models.CharField(max_length=16)
    ip_address = models.IPAddressField(default="127.0.0.1")
    protocol = models.ForeignKey(CommunicationProtocol, null=True, blank=True)
    port = models.PositiveIntegerField(null=True, blank=True)
    
    def get_url(self):
        """Reconstruct :class:`FileServer` URL from attributes."""
        url = ''
        if self.protocol and self.ip_address :
            url += "%s://%s%s/" % (self.protocol.initials.lower(), self.ip_address, '' if not self.port else ":%s" % self.port)
        return url
    url = property(get_url) 
    
    def __unicode__(self):
        return self.label
    
    class Meta:
        ordering = ['protocol', 'ip_address', 'port']

class FileLocation(models.Model):
    """Path on a :class:`FileServer` where a :class:`File` is located."""
    server = models.ForeignKey(FileServer)
    drive = models.CharField(max_length="2", null=True, blank=True)
    root = models.TextField(null=True, blank=True)
    path = models.TextField()
    
    def get_path(self):
        """Reconstruct :class:`FileLocation` path from attributes."""
        st = ''
        if self.drive :
            st += self.drive
        if self.root :
            slashing = "/" if not self.drive else "\\"
            st += (self.root + slashing)
        st += self.path
        return st
    hdd_path = property(get_path)
    
    def get_url(self):
        """Reconstruct :class:`FileLocation` URL from attributes."""
        url = self.server.url + self.hdd_path
        return url
    url = property(get_url) 
    
    def __unicode__(self):
        return self.url
    
    class Meta:
        ordering = ['server', 'root', 'path']

class File(models.Model) :
    """File containing data."""
    name = models.TextField()
    location = models.ForeignKey(FileLocation, null=True) 
    mimetype = models.ForeignKey(MimeType, null=True)
    original = models.NullBooleanField(null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_filename(self):
        """Get the complete filename of a :class:`File`."""
        st = self.name
        if self.mimetype :
            st += '.' + self.mimetype.extension
        return st
    filename = property(get_filename)
    
    def is_available(self):
        """Tell if a :class:`File` is actually on hard disk drive."""
        results = find_file(self.location.hdd_path, self.filename)
        return (len(results) == 1)
    
    def get_all_file_formats(self):
        """Get all available file formats for a :class:`File`."""
        dct = SortedDict()
        pattern = "%s.*" % self.name
        results = find_file(self.location.hdd_path, pattern)     
        for path in results :
            format = path.split('.')[-1].lower()
            dct[format] = path
        return dct
    formats = property(get_all_file_formats)
    
    def get_protocol(self):
        """Get executed protocol name that has generated a :class:`File`."""
        signals = self.signal_set.filter(protocol__isnull=False).distinct()
        if signals.count() :
            return signals[0].protocol
        else :
            return None
    protocol = property(get_protocol)
    
    def get_protocols(self):
        """Get :class:`ProtocolRecording` objects relative to a :class:`File`."""
        protocols = self.signal_set.filter(channel__protocol__isnull=False).distinct()
        return protocols
    protocols = property(get_protocols)
    
    def get_protocols_by_type(self):
        """Store protocols relative to the block by protocol type."""
        protocols = {}
        for protocol in self.get_protocols() :
            name = protocol.protocol_type.label
            if not (name in protocols) :
                protocols[name] = []
            protocols[name].append(protocol)
        #transform each list of protocol into a QuerySet
        for protocol in protocols :
            protocols[protocol] = self.protocolrecording_set.model.objects.filter(pk__in=[k.pk for k in protocols[protocol]])
        return protocols
    
    def get_protocol_types(self):
        """Get all protocol types."""
        protocols = self.get_protocols_by_type().keys()
        return protocols
    distinct_protocols = property(get_protocols)
    
    def _protocols(self):
        """Get comma separated protocol names."""
        protocols = self.get_protocols()
        return ','.join(protocols) if protocols else None
    protocol_names = property(_protocols)
    
    def get_path(self, format=None):
        """Get the actual path to a :class:`File`."""
        if not format :
            return "%s/%s.%s" % (self.location.hdd_path, self.name, self.mimetype.extension) 
        else :
            return self.formats.get(format.lower(), None)  
    hdd_path = property(get_path)
    
    def is_available_as(self, format):
        """Tell if the :class:`File` is available as the specified format."""
        return format.lower() in self.formats
    
    def __unicode__(self):
        return self.filename
    
    class Meta:
        ordering = ['name', 'mimetype']
