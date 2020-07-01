#!/usr/bin/env bash
# set -x

ZIPFILE='exported_file_from_slack.zip'

# Note that we don't use unzip -l to list files in the zip, as it does not
# handle character encoding well. If you're sure all your channels and usernames
# are ASCII, unzip -l should work safely for you. Otherwise, lsar is safer.
# ZIP_LIST_TOOL='/usr/local/bin/lsar'
ZIP_LIST_TOOL='/usr/bin/unzip -Z1'

# A Slack export has the following meta files in the root of the extracted directory:
#   dms.json - Direct messages
#   users.json - User accounts
#   integration_logs.json
#   groups.json - private channel meta information
#   channels.json - public channel meta information
#   mpims.json

# Make sure we're in UTF-8...
LANG="ie_EN.UTF-8"
LC_COLLATE="ie_EN.UTF-8"
LC_CTYPE="ie_EN.UTF-8"
LC_MESSAGES="ie_EN.UTF-8"
LC_MONETARY="ie_EN.UTF-8"
LC_NUMERIC="ie_EN.UTF-8"
LC_TIME="ie_EN.UTF-8"
LC_ALL="ie_EN.UTF-8"

## # Extract the key json files with meta data...
for i in 'groups.json' 'channels.json' 'dms.json' 'mpims.json'
do
  echo -n "Extracting ${i} from ${ZIPFILE}..."
  unzip -p "${ZIPFILE}" "${i}" > "${i}"
  echo "done"
done

# Replaced with python2 script, which handles UTF-8 correctly...
## echo -n "Generating a list of all folders and files contained in ${ZIPFILE}..."
## ${ZIP_LIST_TOOL} "${ZIPFILE}" > 'filelist.txt'
## echo "done"
echo "Please run list_zipfile_contents.py"
