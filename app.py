import requests
import os
import logging
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler

load_dotenv()
zone_id = os.getenv("ZONE_IDENTIFIER")
api_email = os.getenv("API_EMAIL")
api_key = os.getenv("API_KEY")

headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": api_email,
    "X-Auth-Key": api_key
}

logger = logging.getLogger("log")
logger.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_filename = "dns_update_log"
handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7, encoding="utf-8")
handler.setFormatter(log_format)
logger.addHandler(handler)

def update_dns_records(current_ip):
    list_dns_records_endpoint = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    dns_records_result = requests.get(list_dns_records_endpoint, headers=headers)
    data = dns_records_result.json()
    result_data = data.get("result", [])
    length_of_result = len(result_data)
    dns_record_list = []
    for i in range(length_of_result):
        record = {
            "id": result_data[i]["id"],
            "name": result_data[i]["name"],
            "type": result_data[i]["type"],
        }
        dns_record_list.append(record)
    for record in dns_record_list:
        if record["type"] == "CNAME" or record["type"] == "SRV":
            continue
        patch_dns_records_endpoint = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}"
        payload = {
            "content": current_ip
        }
        patch_response = requests.request("PATCH", patch_dns_records_endpoint, json=payload, headers=headers)
        if patch_response.status_code == 200:
            logger.info("Updated record: %s", record['name'])
        else:
            logger.error(patch_response.status_code, patch_response.text)

if __name__ == "__main__":
    file_path = 'IPv4_address.txt'
    if os.path.exists(file_path):
        logger.info(f"The file '{file_path}' exists.")
    else:
        with open(file_path, 'w') as file:
            file.write("0.0.0.0")
    with open(file_path, 'r') as file:
        cached_ip = file.read()
    current_ip_url = "https://ipv4.icanhazip.com/"
    try:
        current_ip = requests.get(current_ip_url)
        current_ip.raise_for_status()
        current_ip = current_ip.text.rstrip()
        logger.info("Cached IP is: " + cached_ip + " current IP is: " + current_ip)
    except requests.RequestException as e:
        logger.error(f"Error making the request: {e}")
    if (cached_ip != current_ip):
        logger.info("IP has changed, updating DNS records...")
        update_dns_records(current_ip)
        with open(file_path, 'w') as file:
            file.write(current_ip)
    else:
        logger.info("IP has not changed.")
