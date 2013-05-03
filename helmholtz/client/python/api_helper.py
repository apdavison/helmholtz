#encoding:utf-8

# API CLIENT
# simple api functions to get and retrieve data from helmholtz 
# using its RESTful API

import sys
import urlparse
import json
import datetime

# additional modules required for this client
import requests
import neo


class dataImporter( ) :

    def __init__( self, ip, authorization_code ) :
        self.ip = ip
        self.auth = authorization_code

    def get_resource( self, resource_uri ) :
        request = requests.get( resource_uri, headers={'Authorization':'Basic ' + self.auth} )
        if request.status_code != 200 :
            print >> sys.stderr, "Request Error:" + str(request.status_code)
            sys.exit()  
        return request
        
    def post_resource( self, resource_url, payload ) :
        heads = {'Content-Type':'application/json', 'Authorization':'Basic '+self.auth }
        request = requests.post( resource_url, data=payload, headers=heads )
        # check creation success
        if request.status_code != 201 and request.status_code != 202 :
            print >> sys.stderr, "Request Invalid Status Code:" + str(request.status_code)
            print >> sys.stderr, "\nText:" + request.text
            print >> sys.stderr, "\nRequest Headers:"
            print >> sys.stderr, request.request.headers
            print >> sys.stderr, "\nResponse Headers:" 
            print >> sys.stderr, request.headers
            sys.exit()  
        # get new resource uri
        parsed = urlparse.urlparse( request.headers['location'] )
        uri = parsed.path
        return uri

    # importer of recording data via Neo
    def importRecordingFile( self, cls, filename, experiment, recordingblock, location, stimulus, mimetype ) :
        self.neoClass = cls
        # if the experiment exists attach to it, otherwise complain
        exp_uri = '/experiment/experiment/'+experiment+'/'
        self.get_resource( 'http://'+self.ip+exp_uri )
        # if the recording block exists attach to it, otherwise complain
        blk_uri = '/recording/recordingblock/'+recordingblock+'/'
        self.get_resource( 'http://'+self.ip+blk_uri )
        # open the file using supplied class reference (ex: neo.io.elphyio)
        ef = self.neoClass( filename=filename )
        # resources before file creation should be already there, maybe another function?
        data = json.dumps( { "name":filename, "location":location, "mimetype":mimetype } )
        file_uri = self.post_resource( 'http://'+self.ip+'/storage/file/', data )
        # read block -> create helmholtz protocolrecording
        block = ef.read_block( lazy=False, cascade=True )
        self.importNeoStruct( block, blk_uri, file_uri, stimulus )

    # importer of recording data via Neo
    def importNeoStruct( self, block, blk_uri, file_uri, stim_uri ) :
        # create protocol recording
        data = json.dumps( { 'block':blk_uri, 'name':'protocol recording '+str(block.name), 'file':file_uri, 'stimulus':stim_uri } )
        prot_uri = self.post_resource( 'http://'+self.ip+'/recording/protocolrecording/', data )
        # read segments -> create helmholtz segments
        for segment in block.segments :
            data = json.dumps( { 'recording':prot_uri, 'name':'segment '+str(block.name), 'file':file_uri } )
            segm_uri = self.post_resource( 'http://'+self.ip+'/recording/segment/', data )
            # read analogsignals -> create helmholtz continuoussignal
            for analogsignal in segment.analogsignals :
                data = json.dumps( { 
                    'segment': segm_uri, 
                    'units': str(analogsignal.units).strip(".0123456789 "), 
                    'sampling_rate': analogsignal.sampling_rate.item(), 
                    'file': file_uri, 
                    'name': analogsignal.name, 
                    'start': str(datetime.time( microsecond = int(analogsignal.t_start.item() / 1000) )),
                    'stop': str(datetime.time( microsecond = int(analogsignal.t_stop.item() / 1000) ))
                } )
                as_uri = self.post_resource( 'http://'+self.ip+'/recording/continuoussignal/', data )
                #print as_uri
            # read spiketrains -> create helmholtz discretesignal
            for spiketrain in segment.spiketrains :
                data = json.dumps( { 
                    'segment': segm_uri, 
                    'units': str(spiketrain.units).strip(".0123456789 "), 
                    'sampling_rate': spiketrain.sampling_rate.item(), 
                    'file': file_uri, 
                    'name': spiketrain.name, 
                    'start': str(datetime.time( microsecond = int(spiketrain.t_start.item() / 1000) )),
                    'stop': str(datetime.time( microsecond = int(spiketrain.t_start.item() / 1000) )),
                    'waveform_description': str(spiketrain.waveform), 
                    'left_sweep': spiketrain.left_sweep.item() 
                } )
                st_uri = self.post_resource( 'http://'+self.ip+'/recording/discretesignal/', data )
                #print st_uri
        # read recordingchannels -> create corresponding helmholtz structures
        for rcg in block.recordingchannelgroups :
            for recordingchannel in rcg :
                # get all analogsignals for this recording channel
                as_uris = []
                for asig in recordingchannel.analogsignals :
                    #as_uris.append(  )
                    pass
                data = json.dumps( { 
                    'protocol': prot_uri, 
                    'index': recordingchannel.index, 
                    'name': recordingchannel.name, 
                    'file': file_uri, 
                    #'continuous_signals': [],
                    #'configuration': 
                } )
                rc_uri = self.post_resource( 'http://'+self.ip+'/recording/continuoussignal/', data )
                #print recordingchannel
        return True


###############################################################
# Test

#im = dataImporter( ip='127.0.0.1', authorization_code='ZG86ZG8=' )

# import recording data starting from an Elphy File
#im.importRecordingFile( neo.io.ElphyIO, "/home/do/helmholtz/helmholtz/ElphyExample_Mode1.dat" )

# import data from an already existing Neo block structure 
#blk_uri = '/recording/recordingblock/1/'
#data = json.dumps({"name":,"location":"/storage/filelocation/1/","mimetype":"/storage/mimetype/pdf/"})
#file_uri = im.post_resource( 'http://'+im.ip+'/storage/file/', data )
#im.importNeoStruct( block, blk_uri, file_uri )

