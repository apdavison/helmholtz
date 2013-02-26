#encoding:utf-8

import api_helper
import neo

# Test

im = api_helper.dataImporter( ip='127.0.0.1', authorization_code='ZG86ZG8=' )

# import recording data starting from an Elphy File
#im.importRecordingFile( neo.io.ElphyIO, "/home/do/helmholtz/helmholtz/client/ElphyExample_Mode1.dat" )

# import data from an already existing Neo block structure 
#blk_uri = '/recording/recordingblock/1/'
#data = json.dumps({"name":,"location":"/storage/filelocation/1/","mimetype":"/storage/mimetype/pdf/"})
#file_uri = im.post_resource( 'http://'+im.ip+'/storage/file/', data )
#im.importNeoStruct( block, blk_uri, file_uri )

# controllers
# get entity by filter name

# execution

