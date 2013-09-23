#encoding:utf-8

import glob
import json

import api_helper
import neo

# Test

im = api_helper.dataImporter( ip='127.0.0.1', authorization_code='ZG86ZG8=' )

#prefix = "/var/www/brainscales_db/data/103/"
prefix = "/var/www/brainscales_db/data/4/"
for filename in glob.glob( prefix+'*.dat' ) :
    filename = filename.replace( prefix, '' )
    print filename
    if 'name' in filename :
        exp = "2"
        rb = "2"
        fl = "/storage/filelocation/1/"
        if "10.dat" in filename :
            st = "/stimulation/stimulus/4/"
        if "50.dat" in filename :
            st = "/stimulation/stimulus/5/"
        if "100.dat" in filename :
            st = "/stimulation/stimulus/6/"
    if '2308D' in filename :
        exp= "103"
        rb = "636"
        fl = "/storage/filelocation/39/"
        st = "/stimulation/stimulus/38/"
    if '2308G' in filename :
        exp= "103"
        rb = "636"
        fl = "/storage/filelocation/72/"
        st = "/stimulation/stimulus/71/"

    # parse filename into protocol
    # name=FullfieldDriftingSinusoidalGrating#sheet_name=V1_Exc_L4#orientation=0.0#contrast=10.dat
    #split #
    #    split =
    #        name = FullfieldDriftingSinusoidalGrating
    #       sheet_name = V1_Exc_L4
    #       orientation = 0.0
    #       contrast = 10
    print "exp:%s   recblock:%s   file:%s   stim:%s" % (exp, rb, fl, st)

    # import recording data starting from an Elphy File
    im.importRecordingFile( 
        neo.io.ElphyIO, 
        prefix+filename, 
        experiment=exp, 
        recordingblock=rb, 
        location=fl, 
        stimulus=st,
        mimetype="/storage/mimetype/dat/" 
    )
