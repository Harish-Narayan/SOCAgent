import requests
import os
from config import API_KEY  # Import the API key from config.py
from dotenv import load_dotenv, dotenv_values 
dotenv_path = 'secrets.env'
load_dotenv(dotenv_path)
def get_ip_info(ip_address):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }

    response = requests.get(url, headers=headers)
    return response.text

# Example usage
ip_address = "188.114.97.3"  # Replace this with the IP address you want to query
response_text = get_ip_info(ip_address)
print(response_text)
