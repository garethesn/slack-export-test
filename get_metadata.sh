#!/usr/bin/env bash
# set -x

# USAGE: Pass in the Slack Export ZIP file as the first and only argument.
#   If not argument is passed, it will try and find the export zip file at
#   ./exported_file_from_slack.zip

ZIPFILE=${1:-'exported_file_from_slack.zip'}
echo "Slack Archive => '${ZIPFILE}'"

# Note that we don't use unzip -l to list files in the zip, as it does not
# handle character encoding well. If you're sure all your channels and usernames
# are ASCII, unzip -l should work safely for you. Otherwise, lsar is safer.
# Update: lsar on OS X does not appear to handle Zip files larger than 2GB, so
# we use some python2 unzip code (with thanks to @nsheridan)

# ZIP_LIST_TOOL='/usr/local/bin/lsar'
# ZIP_LIST_TOOL='/usr/bin/unzip -Z1'
ZIP_LIST_TOOL='../../../git/slack-export-test/list_zipfile_contents.py'


if [ -r "${ZIPFILE}" ];
then
  # A Slack export has the following meta files in the root of the extracted directory:
  #   dms.json - Direct messages
  #   users.json - User accounts
  #   integration_logs.json
  #   groups.json - private channel meta information
  #   channels.json - public channel meta information
  #   mpims.json

  # Extract the key json files with meta data...
  for i in 'groups.json' 'channels.json' 'dms.json' 'mpims.json'
  do
    echo -n "Extracting ${i} from ${ZIPFILE}..."
    unzip -p "${ZIPFILE}" "${i}" > "${i}"
    echo "done"
  done

  # Replaced with python2 script, which handles UTF-8 correctly...
  echo -n "Generating a list of all folders and files contained in ${ZIPFILE}..."
  ${ZIP_LIST_TOOL} "${ZIPFILE}"
  echo "done"
else
  echo "ERROR! Slack export ZIP archive '${ZIPFILE}' was not found, or is not readable."
  echo "Usage: ./get_metadata.sh <exported_zip_file_from_slack_export.zip"
  echo
fi
