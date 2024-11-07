import requests
import pandas as pd
import io
import time
GENESYS_CLOUD_CLIENT_ID = 'd17da951-cc19-438c-98b1-5b91db75205f'
GENESYS_CLOUD_CLIENT_SECRET = 'ReOAwXdhVgTe8rLC9cXr1wuNnfnVV4gNE201OikrnC0'
CONTACT_LIST_ID = '29d520ba-e091-4976-bb0b-c8d4fd605bf8' 

def get_access_token():
    token_url = "https://login.mypurecloud.de/oauth/token"
    token_payload = {
        "grant_type": "client_credentials",
        "client_id": GENESYS_CLOUD_CLIENT_ID,
        "client_secret": GENESYS_CLOUD_CLIENT_SECRET
    }
    token_response = requests.post(token_url, data=token_payload)
    token_response.raise_for_status()
    return token_response.json()["access_token"]
def get_data(access_token):
    data_url = "https://api.mypurecloud.de/api/v2/downloads/eef29903ea884dee"
    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data_response = requests.get(data_url, headers=api_headers)
    data_response.encoding = 'utf-8-sig'  # Handle BOM
    # Check the response content type
    if 'application/json' in data_response.headers.get('Content-Type', ''):
        data = data_response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print("Response content is not in JSON format")
        data = data_response.text
        df = pd.read_csv(io.StringIO(data))
        return df
def initiate_export(access_token):
    export_url = f"https://api.mypurecloud.de/api/v2/outbound/contactlists/{CONTACT_LIST_ID}/export"
    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    export_payload = {
        "exportFormat": "CSV"  # Include additional required fields if any
    }
    export_response = requests.post(export_url, headers=api_headers, json=export_payload)
    if export_response.status_code == 200:
        print("Export initiated successfully")
    else:
        print(f"Failed to initiate export: {export_response.status_code}, {export_response.text}")

        
time.sleep(10)
access_token = get_access_token()
# Highlighted code
initiate_export(access_token)
data = get_data(access_token)
print(data)