
import requests
from bs4 import BeautifulSoup
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


URL = 'https://www.bookyogaretreats.com/'

# Replace 'YOUR_JSON_FILE.json' with the path to your downloaded credentials JSON file
SERVICE_ACCOUNT_FILE = './google-service.json'

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and create the gspread client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Replace with your Google Sheet ID and Sheet name
SPREADSHEET_ID = '1BDUlk5AWnc3A_j3XQm7_C9i8PL_uOo22fBBYXHugcw0'
SHEET_NAME = 'Sheet1'

def scrape_book_yoga_retreats():
    try:
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'authority': 'www.bookyogaretreats.com'
        })
        print('headerss', headers)
        response = requests.get(URL, headers=headers)
        print(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        retreats = []
        print('soup',soup.find('div', attrs={'class': 'showcard-listing-content'}))
        for item in soup.select('.showcard-listing-content'):
            name = item.select_one('.listing-title').get_text(strip=True)
            location = item.select_one('.pre-main-content__location').get_text(strip=True)
            price = item.select_one('.price').get_text(strip=True)
            retreats.append({'name': name, 'location': location, 'price': price})
    
        return retreats
    except Exception as e:
        print('e', e)

def save_to_google_sheets(data):
    # Implement Google Sheets API logic here
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        print('sheet', data.columns.values, data['name'].values)
        # Convert DataFrame to a list of lists
        values = [data.columns.values.tolist()] + data.values.tolist()
        
        # Clear the existing content in the sheet
        sheet.clear()

        # Update the sheet with the data
        sheet.update(values)
        print("Data successfully written to Google Sheets.")
    except Exception as e:
        print(e)
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    retreats = scrape_book_yoga_retreats()
    df = pd.DataFrame(retreats)
    print(df)
    save_to_google_sheets(df)
