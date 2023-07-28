# Dynamic DNS Update Script

My ISP changes my IP-address at random intervals. This can get annoying when hosting a services open to the internet. To combat this I have registered a domain with Cloudflare and written this script that makes a request to icanhazip.com to check what the current IP address is. If it is different than last time the script was run it updates all the DNS records programatically through the Cloudflare API. First, it makes a GET request to fetch all of the DNS records and then sends a PATCH request to update every single one. The script logs to a file named 'dns_update_log'. There are kept 7 days of logs.

If you wish to use this script: 

```bash
mv .env.example .env
```

Update to reflect your values.

If you wish to add it is a cron-job to run every minute you can add the following line:

```bash
crontab -e
```

```bash

```

