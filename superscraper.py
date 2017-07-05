#!venv/bin/python3

"""
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
"""

from datetime import datetime

from bs4 import BeautifulSoup
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import KEYFILE_NAME, SPREADSHEET_NAME, WORKSHEET_INDEX

# this is the basic url, there's other ways to grab the data
# but it's messy and outside my scope for now
QSUPER_URL = "https://qsuper.qld.gov.au/performance/unit-prices/"

GOOGLE_CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE_NAME, ['https://spreadsheets.google.com/feeds'])

DEBUG = False

def main():
    PAGE = requests.get(QSUPER_URL)
    # parse the HTML
    SOUPER = BeautifulSoup(PAGE.text, "html.parser")
    # look for the unit price div
    unitpricediv = SOUPER.find(id=r"pw_phbody_0_pw_phmain_0_pnlUnitPrices")

    # don't pull worksheet data until we've checked we have the unit prices, it's slow
    if unitpricediv:
        # log in to google
        GOOGLE_OBJECT = gspread.authorize(GOOGLE_CREDENTIALS)
        # open the worksheet
        worksheet = GOOGLE_OBJECT.open(SPREADSHEET_NAME).get_worksheet(WORKSHEET_INDEX)
        if DEBUG: print("Opened SuperUnitPrices Spreadsheet, pulling records...",)
        RECORDS = worksheet.get_all_records(empty2zero=False, head=1, default_blank='')
        VALIDROWS = [record for record in RECORDS if record['Date'] != ""]
        if DEBUG: print("done.")

        # filter out the dates from the spreadsheet
        DATES_IN_WORKSHEET = [row['Date'] for row in VALIDROWS]

        # process the qsuper table
        rows_added = 0
        for row in unitpricediv.table.find_all('tr'):
            if row.td:
                # skip the header row, because yeah.
                tds = [td.contents for td in row.find_all('td')]
                # parse the date cell
                #example: Friday, 03 March 2017
                dateval = datetime.strptime(tds[0][0], "%A, %d %B %Y")
                # convert the value cell
                val = float(tds[-1][0])
                # check if the row exists already in the spreadsheet
                if dateval.strftime('%d/%m/%Y') in DATES_IN_WORKSHEET:
                    pass
                else:
                    # don't have data for this one.
                    newrow = (dateval.strftime('%d/%m/%Y'), val, '')
                    if DEBUG: print("Adding new row: {}".format(newrow))
                    worksheet.append_row(newrow)
                    rows_added += 1
    else:
        if DEBUG: print("Couldn't pull unit prices from {}".format(QSUPER_URL))

    if rows_added:
        if DEBUG: print("Added {} new data points".format(rows_added))
    else:
        if DEBUG: print("No new data.")

if __name__ == '__main__':
    main()
