#!/usr/bin/env bash
# set -x

ZIPFILE='exported_file_from_slack.zip'

# A Slack export has the following meta files in the root of the extracted directory:
#   dms.json - Direct messages
#   users.json - User accounts
#   integration_logs.json
#   groups.json - private channel meta information
#   channels.json - public channel meta information
#   mpims.json

# Extract the key json files with meta data...
for i in 'groups.json' 'channels.json' 'dms.json'
do
  echo -n "Extracting ${i} from ${ZIPFILE}..."
  unzip -p "${ZIPFILE}" "${i}" > "${i}"
  echo "done"
done

echo -n "Generating a list of all folders and files contained in ${ZIPFILE}..."
unzip -Z1 "${ZIPFILE}" > 'filelist.txt'
echo "done"
echo
