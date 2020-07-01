#!/usr/bin/python3

# Imports...
import json

# Constants and definitions...
slack_privatechannels_meta_file = 'groups.json'
slack_publicchannels_meta_file  = 'channels.json'
slack_dms_meta_file             = 'dms.json'
slack_export_filelist           = 'filelist.txt'

slack_channels = {}     # The slack channels expected from the meta json file
files = {}              # The actual folders and count of files per folder found in the zip archive
errors = ''             # We'll store all errors and print them at the end


#######################################################################
# Read the folders and count of files in folders into a dict...
#
f = open(slack_export_filelist, 'r', encoding='iso8859')

folder_count = 0
files_count = 0

for line in f:
    line = line.strip()
    if( line[-1:] == '/' ):
        # This is a folder since it ends in a slash...
        folder_name = line[:-1]     # Strip the trailing slash
        if(folder_name in files):
            errors += "ERROR! : Duplicate folder '{}' found in zip file.\n".format(folder_name)
        else:
            files[line[:-1]] = 0
        folder_count += 1
    elif( '/' in line[:-1] ):
        # This is not a folder, and must be a file within a folder...
        folder_name,file = line.split('/', 1)
        if( folder_name in files ):
            files[folder_name] += 1
            # print("--> folder name: {}   |  file count: {}".format(folder_name, files[folder_name]))
        files_count += 1
    else:
        # Likely a bare file. Add it to errors string, so we can validate...
        errors += "INFO: Found bare file (in root directory of zip): '{}'\n".format(line)
f.close()



#######################################################################
# Read the channels from the json file into a dict...
#
f = open(slack_privatechannels_meta_file, 'r', encoding='utf-8')
json_data = json.loads(f.read())

channel_count = 0

for list_item in json_data:
    for key, value in list_item.items():
        channel_id   = list_item['id']
        channel_name = list_item['name']
        if(channel_name in slack_channels):
            if(slack_channels[channel_name] != channel_id):
                # We've found channels with duplicate names, but NOT duplicate IDs...
                errors += "ERROR! : Found channels '{}' with duplicate name in json file {} : {}".format(channel_name, slack_channel_meta_file)
        else:
            slack_channels[channel_name] = channel_id
            channel_count += 1

        # print( "DEBUG: json id: '{}' | channel name: '{}'".format(channel_id, channel_name) )


#######################################################################
# Print some useful output...
#
print(errors)
print("INFO: from file list: Found {} folders and files dict has {} folders (these numbers should match!)".format(folder_count, len(files)))
print("INFO: from json meta: Index contains {} channels, of {} channels found (should match the number of folders in file list.)".format(len(slack_channels), channel_count))
