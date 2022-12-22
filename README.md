<!-- [![get-and-update-verified-bots-list](https://github.com/BrooksCunningham/tfc-verified-bots/actions/workflows/python_cron.yml/badge.svg?branch=main)](https://github.com/BrooksCunningham/tfc-verified-bot/actions/workflows/python_cron.yml) -->

# tfc-verified-bots
Terraform GCP IPs

This repo will get the latest Googlbot ips and update a list with Fastly's Next-Gen WAF. Github actions perform the following tasks: 
* Pull the GCP IP list as a cron
* Update the repo with the latest Googlbot IPs and use Terraform cloud to update the IP list in Fastly's Next-Gen WAF.


# What's next?
* Bingbot IPs
