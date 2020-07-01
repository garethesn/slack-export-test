#!/usr/bin/python3

# Imports...
import json

# Constants and definitions...
slack_privatechannels_meta_file = 'groups.json'
slack_publicchannels_meta_file  = 'channels.json'
slack_dms_meta_file             = 'dms.json'
slack_mpims_meta_file           = 'mpims.json'
slack_export_filelist           = 'filelist.txt'

# Global variables, because who doesn't love a good global variable?...
slack_private_channels = {}     # The slack private channels expected from the meta json file
slack_public_channels = {}      # The slack public channels expected from the meta json file
slack_dm_channels = {}          # The DMs expected from the meta json file
slack_mpims_channels = {}       # The MPIMs (Multi-Party IMs???) from the meta json file
files = {}                      # The actual folders and count of files per folder found in the zip archive
errors = ''                     # We'll store all errors and print them at the end



#######################################################################
# Read the Slack JSON meta data into a dict...
#
# channel_filename : path to a JSON file of Slack channel or DM data
# type : public | private | mpim | dm - because the channel JSON uses different keys for DMs
# channel_dict : reference to a dict that will store the channel names and IDs read from the file
#
def import_channel_data(channel_filename, type, channel_dict):
    # open the passed in filename...
    f = open(channel_filename, 'r', encoding='utf-8')
    json_data = json.loads(f.read())

    channel_count = 0

    # Iterate over the JSON objects, and grab the names and channel IDs...
    for list_item in json_data:
        for key, value in list_item.items():
            channel_id   = list_item['id']
            if( type == 'dm' ):
                # DMs do not have a name in the json file...
                channel_name = channel_id
            else:
                channel_name = list_item['name']
            if(channel_name in channel_dict):
                if(channel_dict[channel_name] != channel_id):
                    # We've found channels with duplicate names, but NOT duplicate IDs...
                    errors += "ERROR! : Found channels '{}' with duplicate name in json file {}".format(channel_name, channel_filename)
            else:
                channel_dict[channel_name] = channel_id
                channel_count += 1

            # print( "DEBUG: json id: '{}' | channel name: '{}'".format(channel_id, channel_name) )

    f.close()

    # Return the number of channels discovered (and the populated dict, by reference)...
    return channel_count



#######################################################################
# Read data from each of the JSON meta files into dicts...
#
private_channel_count = import_channel_data(slack_privatechannels_meta_file, 'private', slack_private_channels)
public_channel_count  = import_channel_data(slack_publicchannels_meta_file, 'public', slack_public_channels)
dm_count = import_channel_data(slack_dms_meta_file, 'dm', slack_dm_channels)
mpim_channel_count = import_channel_data(slack_mpims_meta_file, 'mpim', slack_mpims_channels)



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
# Print some useful output...
#
print(errors)
print("INFO: from file list: Found {} folders and files dict has {} folders (these numbers should match!)".format(folder_count, len(files)))
print("INFO: from json meta: Private channels indexed {} channels, of {} channels found.".format(len(slack_private_channels), private_channel_count))
print("INFO: from json meta: Public channels indexed {} channels, of {} channels found.".format(len(slack_public_channels), public_channel_count))
print("INFO: from json meta: MPIM channels indexed {} channels, with {} channels found.".format(len(slack_mpims_channels), mpim_channel_count))
print("INFO: from json meta: DMs indexed {} channels, of {} channels found.".format(len(slack_dm_channels), dm_count))
total_channel_meta_count = private_channel_count + public_channel_count + dm_count
if( total_channel_meta_count == folder_count ):
    print("--> total files (from zipfile): {}  |  total channels (from JSON files): {} (they match!)".format(folder_count, total_channel_meta_count))
else:
    print("--> total files (from zipfile): {}  |  total channels (from JSON files): {} (ERROR! These numbers should match)".format(folder_count, total_channel_meta_count))
    if( folder_count > total_channel_meta_count ):
        print("--> ZIP file has an additional {} folders I cannot account for.".format(folder_count - total_channel_meta_count))
    else:
        print("--> META files have an additional {} channels that have no matching folders in the ZIP file.".format(total_channel_meta_count - folder_count))

exit()
