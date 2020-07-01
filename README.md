# slack-export-test
Validation testing for Slack's data export

Specifically, this set of tools attempts to heuristically validate that a Slack export contains all the channels you expect it to contain, and that channel _(and DM)_ folders contain some data. This script never looks at the contents of any messages or DMs.


## Usage
1. Export from Slack, using the export utility, and download the generated ZIP file
1. Edit `get_metadata.sh` and insert the name of your ZIP file.
1. Run `bash get_metadata.sh` This will extract the JSON metadata files and output a list of all the files and folders in the ZIP archive. The next script will use only these generated files for analysis.
1. Run `python3 analyze_slack_export.py` and interpret the results.


## A note on privacy
A Slack export is intended for the purposes of migration, backup, and legal discovery. As such, an export contains an unencrypted and unsecured copy of the data from your Slack instance - including private channels and DMs. You should treat any export files with extreme care and securely delete them as soon as you no longer need them.

This script is specifically designed to run and heuristically guess whether an export has completed and contains all the information you might expect it to contain. It very deliberately does not look into any of the JSON files that contain messages, attachments, DMs, etc.

However, meta data can contain private and confidential information - such as the knowledge that at some point in time, person A had a private conversation with person B. Channel names _(both public and private)_ are also exposed in meta data, so if you have a private channel named `marys-surprise-birthday-party` and Mary has access to the meta data, she might get a clue that something is being planned - and by parsing the `users.json` file can determine who is planning behind her back.

In summary, this attempts to be as careful as possible re exposure and reading of sensitive data. However, you should still take extreme care with any export ZIP file, or meta data extracted from it.
