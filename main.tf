# Terraform 0.13.x
terraform {
  cloud {
    organization = "bcunning"
    workspaces {
      tags = ["googlebot"]
    }
  }
  required_providers {
    sigsci = {
      source = "signalsciences/sigsci"
    }
  }
}

variable "SIGSCI_CORP" {
    type        = string
    description = "This is the corp where configuration changes will be made as an env variable."
}
variable "SIGSCI_EMAIL" {
    type        = string
    description = "This is the email address associated with the token for the Sig Sci API as an env variable."
}
variable "SIGSCI_TOKEN" {
    type        = string
    description = "This is a secret token for the Sig Sci API as an env variable."
}
variable "GOOGLEBOT_IP_LIST" {
    type        = list
    description = "Used for a list of Googlebot IPs, https://developers.google.com/static/search/apis/ipranges/googlebot.json"
}

provider "sigsci" {
  corp = "${var.SIGSCI_CORP}"
  email = "${var.SIGSCI_EMAIL}"
  auth_token = "${var.SIGSCI_TOKEN}"
}

resource "sigsci_corp_list" "googlebot_ips_list" {
  name        = "Googlebot IPs list"
  type        = "ip"
  description = "Outbound Googlebot IPs"
  entries = "${var.GOOGLEBOT_IP_LIST}"
}
