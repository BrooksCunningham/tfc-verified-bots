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
    fastly = {
      source  = "fastly/fastly"
      version = ">= 3.0.4"
    }
  }
}

# Fastly Edge VCL configuration
variable "FASTLY_API_KEY" {
    type        = string
    description = "This is API key for the Fastly VCL edge configuration."
}

provider "fastly" {
  api_key = "${var.FASTLY_API_KEY}"
}

variable "googlebot_ip_dictionary" {
  type    = object({ name = string, items = map(string) })
  default = {
    name  = "googlebot IP dictionary"
    items = {}
  }
}

resource "fastly_service_dictionary_items" "items" {
  for_each = {
  for d in fastly_service_vcl.verified-bots-demo-service.dictionary : d.name => d if d.name == var.googlebot_ip_dictionary.name
  }
  service_id = fastly_service_vcl.verified-bots-demo-service.id
  dictionary_id = each.value.dictionary_id

  items         = var.googlebot_ip_dictionary.items
}

resource "fastly_service_vcl" "verified-bots-demo-service" {
  name = "verified-bots-demo"

  domain {
    name    = "verified-bots-demo.brookscunningham.com"
    comment = "demo"
  }

  backend {
    address = "httpbin.org"
    name    = "httpbin"
    port    = 443
  }

  dictionary {
    name       = var.googlebot_ip_dictionary.name
  }

  force_destroy = true
}


### NGWAF configuration
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
  entries = "${var.googlebot_ips_list}"
}
