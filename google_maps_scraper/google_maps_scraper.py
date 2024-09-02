
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Replace 'YOUR_JSON_FILE.json' with the path to your downloaded credentials JSON file
SERVICE_ACCOUNT_FILE = './google-service.json'

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and create the gspread client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Replace with your Google Sheet ID and Sheet name
SPREADSHEET_ID = '1naBfFd3icx37TOFsQzSsNLqq37fIMR0rWSw9tupBrks'
SHEET_NAME = 'Sheet1'

API_KEY = '' # Replace with your API key
SEARCH_QUERY = 'yoga studios and schools in Thailand'
URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

def fetch_locations(query):
    try:
        response = requests.get(URL, params={'query': query, 'key': API_KEY})
        return response.json()
    except:
        print("An exception occurred")
    

def save_to_google_sheets(data):
    # Implement Google Sheets API logic here
    try:
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

        # Convert DataFrame to a list of lists
        values = [data.columns.values.tolist()] + data.values.tolist()
        
        # Clear the existing content in the sheet
        sheet.clear()

        # Update the sheet with the data
        sheet.update(values)
        print("Data successfully written to Google Sheets.")
    except Exception as e:
        print(f"An error occurred: {e}")
    # pass

if __name__ == "__main__":
    locations = fetch_locations(SEARCH_QUERY)
    df = pd.DataFrame(locations['results'])
    df = df[['name', 'formatted_address']]
    save_to_google_sheets(df)
