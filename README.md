
superscraper pulls the data from the qsuper unit prices page and updates a google spreadsheet.

## Requirements

* Use a virtualenv with the packages from requirements.txt.
* You'll need API keys/oauth data from google developer tools for this. Information here on how to get it - http://gspread.readthedocs.io/en/latest/oauth2.html (Role is Project -> Service Account Actor)
* Make sure you share your google spreadsheet with the email address listed in the .json file.


## Configuration

The script requires you to have two files, config.py and the JSON file from the above service account.

config.py's contents should be as follows:

| Variable | Type | Description |
| --- | --- | --- |
| KEYFILE_NAME | str | the json filename you get from google devtools |
| SPREADSHEET_NAME | str | the name of the spreadsheet in your google account, in the case of duplicate spreadsheet names, the "first" will be used. |
| WORKSHEET_INDEX | int | the nth worksheet in the file - starts at 0 |

