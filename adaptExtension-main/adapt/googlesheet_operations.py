import gspread
from .constants import creds, MASTER_SHEET_NAME, MASTER_LINKEDIN_TAB, MASTER_TAB_NAME


def getInput():
    client = gspread.authorize(creds)
    masterSheet = client.open(MASTER_SHEET_NAME).worksheet(MASTER_TAB_NAME)
    return masterSheet.get_all_records()


def getLinkedinCookies():
    client = gspread.authorize(creds)
    masterSheet = client.open(MASTER_SHEET_NAME).worksheet(MASTER_LINKEDIN_TAB)
    data=masterSheet.get_all_records()
    print(data)
    for each in data:
        if(each['cookies_status']!='expired'):
            return eval(each['cookies']),each['name']



def sheet_data(sheet_name, tab_name):
    """Function will return sheet data and sheet instance so that we can update sheet from other functions"""
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).worksheet(tab_name)

    data = sheet.get_all_records()

    return data, sheet

def upadteEmail(sheet,email,linkedin_url):
    cell = sheet.find(linkedin_url)
    sheet.update_cell(cell.row, cell.col + 6,email)
