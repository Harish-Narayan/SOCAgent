import requests
import json
import os
from dotenv import load_dotenv, dotenv_values 
dotenv_path = 'secrets.env'
load_dotenv(dotenv_path)

def get_ip_info(ip_address):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {
        "accept": "application/json",
        "x-apikey": os.getenv("VT_API_KEY")
    }

    response = requests.get(url, headers=headers).json()
    ip_data=json.dumps(response, indent=4)
    with open('outputs/ip_data.txt', 'w') as file:
        file.write(ip_data)
    return ip_data

def get_domain_info(domain):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    headers = {
        "accept": "application/json",
        "x-apikey": os.getenv("VT_API_KEY")
    }

    response = requests.get(url, headers=headers).json()
    domain_data=json.dumps(response, indent=4)
    with open('outputs/domain_data.txt', 'w') as file:
        file.write(domain_data)
    return domain_data

def get_url_analysis(analysis_id):
    print(analysis_id)
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

    headers = {
        "accept": "application/json",
        "x-apikey": os.getenv("VT_API_KEY")
    }
    analysis_report = requests.get(url, headers=headers).json()
    url_data=json.dumps(analysis_report, indent=4)
    with open('outputs/url_data.txt', 'w') as file:
        file.write(url_data)
    return url_data


def get_url_info(url):
    url = "https://www.virustotal.com/api/v3/urls"
    payload = { "url": f"{url}" }
    headers = {
        "accept": "application/json",
        "x-apikey": os.getenv("VT_API_KEY"),
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers).json()
    # print(f"analysis_id: {response['data']['id']}")
    return get_url_analysis(response['data']['id'])

def get_hash_info(hash):
    url = f"https://www.virustotal.com/api/v3/files/{hash}"

    headers = {
        "accept": "application/json",
        "x-apikey": os.getenv("VT_API_KEY")
    }

    response = requests.get(url, headers=headers).json() 
    hash_data=json.dumps(response, indent=4)
    with open('outputs/hash_data.txt', 'w') as file:
        file.write(hash_data)
    return hash_data

def get_cve_info(cve_id):
    cve=requests.get(f"https://cvedb.shodan.io/cve/{cve_id}").json()
    cve_data = json.dumps(cve, indent=4)
    with open('outputs/cve_data.txt', 'w') as file:
        file.write(cve_data)
    return cve_data




# print(get_ip_info("188.114.97.3" ))
# print(get_cve_info("CVE-2024-36081"))
# print(get_domain_info("www.google.com"))
# print(get_url_info("http://vxvault.net/ViriList.php"))
# print(get_hash_info("9f01d4442c495c7128649b98201187bc0c58dedd"))