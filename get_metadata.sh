#!/usr/bin/env bash
# set -x

ZIPFILE='exported_file_from_slack.zip'

# Note that we don't use unzip -l to list files in the zip, as it does not
# handle character encoding well. If you're sure all your channels and usernames
# are ASCII, unzip -l should work safely for you. Otherwise, lsar is safer.
ZIP_LIST_TOOL='/usr/local/bin/lsar'

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

echo -n "Generating a list of all folders and files contained in ${ZIPFILE}..."
${ZIP_LIST_TOOL} "${ZIPFILE}" > 'filelist.txt-temp'
# Remove the first line, because lsar adds a header line...
tail -n +2 'filelist.txt-temp' > 'filelist.txt'
rm 'filelist.txt-temp'
echo "done"
echo
