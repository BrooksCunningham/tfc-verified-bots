from github import Github
import json
from os import environ

def main():

    def get_googlebot_ips_list():
        import requests
        resp = requests.get('https://developers.google.com/static/search/apis/ipranges/googlebot.json')
        json_response = resp.json()

        ip_prefixes = json_response["prefixes"]

        # googlebot_ip_address_ranges = "["

        googlebot_ip_address_ranges = []

        for ip_prefix in ip_prefixes:
            if "ipv4Prefix" in ip_prefix:
                googlebot_ip_address_ranges.append(ip_prefix["ipv4Prefix"])
            if "ipv6Prefix" in ip_prefix:
                googlebot_ip_address_ranges.append(ip_prefix["ipv6Prefix"])

        return googlebot_ip_address_ranges


    def compare_local_and_github_ip_list(local_list, github_list):
        if local_list == github_list:
            return True
        else:
            return False

    # First create a Github instance:
    # using a personal access token
    # github_access_token = environ.get("GITHUB_ACCESS_TOKEN") # Must use GITHUB_ACCESS_TOKEN for local testings
    github_access_token = environ.get("GITHUB_TOKEN")
    g = Github(github_access_token)

    # Get the repo
    repo = g.get_repo("BrooksCunningham/tfc-verified-bots")

    # Get file in github
    googlebot_ips_file_contents = repo.get_contents("main.auto.tfvars")

    googlebot_ips = get_googlebot_ips_list()
    
    # Format the tf_variable
    tf_var_formatted_googlebot_list = "googlebot_ips_list = " + json.dumps(googlebot_ips, indent=2) + "\n\n"


    formatted_googlebot_fastly_edge_dictionary = {}

    for idx, ip in list(enumerate(googlebot_ips, start=1)):
        formatted_googlebot_fastly_edge_dictionary[idx] = ip

    formatted_googlebot_fastly_edge_dictionary = { "name" : "googlebot ips", "items" : formatted_googlebot_fastly_edge_dictionary }

    tf_var_formatted_googlebot_fastly_edge_dictionary =  "googlebot_ip_dictionary = " + json.dumps(formatted_googlebot_fastly_edge_dictionary, indent=2)

    # print(tf_var_formatted_googlebot_fastly_edge_dictionary)
    # exit()

    # combine both list for NGWAF and Fastly Edge
    tf_var_formatted_googlebot_lists = tf_var_formatted_googlebot_list + tf_var_formatted_googlebot_fastly_edge_dictionary

    print(tf_var_formatted_googlebot_lists)
    exit()

    # Download the file from the remote main branch
    github_googlebot_ips_file_contents_decoded = googlebot_ips_file_contents.decoded_content.decode()

    # compare file contents locally and main branch
    googlebot_ip_list_compare = compare_local_and_github_ip_list(tf_var_formatted_googlebot_lists, github_googlebot_ips_file_contents_decoded)

    if googlebot_ip_list_compare:
        pass
        return "List updated: False"
    else:
        # Update the repo
        repo.update_file(googlebot_ips_file_contents.path
          , "automated GOOGLEBOT_IP_LIST update"
          , tf_var_formatted_googlebot_list
          , googlebot_ips_file_contents.sha
          , branch="main")
        return "List updated: True"

print(main())
