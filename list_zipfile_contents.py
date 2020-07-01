#!/usr/bin/python

# Note that this MUST be run as python 2.
# As at time of writing, zipfile does not work correctly under python3
import zipfile
import sys

ZIPFILE = 'exported_file_from_slack.zip'
filelist_filename = 'filelist.txt'

filelist = ''
file_count = 0

f = open(filelist_filename, 'w')

z = zipfile.ZipFile(ZIPFILE)
for file in z.namelist():
    filelist += u"{}\n".format(file)
    file_count += 1
    if(file_count % 100 == 0):
        f.write(filelist.encode('utf-8'))
        filelist = ''
        print file_count, "...",
        sys.stdout.flush()

# Flush any remaining lines to the output file and close...
f.write(filelist.encode('utf-8'))
f.close()
