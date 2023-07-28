# Dynamic DNS Update Script

My ISP changes my IP-address at random intervals. This can get annoying when hosting a services open to the internet. To combat this I have registered a domain with Cloudflare and written this script that makes a request to icanhazip.com to check what the current IP address is. If it is different than last time the script was run it updates all the DNS records programatically through the Cloudflare API. First, it makes a GET request to fetch all of the DNS records and then sends a PATCH request to update all but the CNAME and SRV ones. The script logs to a file named 'dns_update_log' and rolls over to a new file every midnight. Logs are kept for 7 days. 

If you wish to use this script: 

```bash
git clone https://github.com/leiflundberg/ddns-cloudflare
cd ddns-cloudflare
mv .env.example .env
```

Update `.env` file to reflect your values.

You may add the script to run as a cron job with:

```bash
chmod +x app.py
crontab -e
```
I have set it up to run every minute, like so (remember to update to your path):
```bash
* * * * * cd /home/leif/ddns-cloudlare && /usr/bin/python3 /home/leif/ddns-clouflare/app.py
```
