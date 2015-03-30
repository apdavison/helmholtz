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
    
    def __unicode__(self, *args):
        return self.name
    shortname = property(__unicode__)

    def __str__(self):
        return self.__unicode__(self)


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

    def __str__(self):
        return self.__unicode__()

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

    def __str__(self):
        return self.__unicode__()
    
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
    
    def __unicode__(self):
        return self.filename

    def __str__(self):
        return self.__unicode__()
    
    class Meta:
        permissions = (
            ( 'view_file', 'Can view file' ),
        )
        ordering = ['name', 'mimetype']
