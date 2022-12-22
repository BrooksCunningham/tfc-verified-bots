from github import Github
from os import environ

def main():

    def get_gcp_ips_list():
        import requests
        resp = requests.get('https://developers.google.com/static/search/apis/ipranges/googlebot.json')
        json_response = resp.json()

        ip_prefixes = json_response["prefixes"]

        googlebot_ip_address_ranges = "["

        for ip_prefix in ip_prefixes:
            if "ipv4Prefix" in ip_prefix:
                googlebot_ip_address_ranges = googlebot_ip_address_ranges + '\"' + ip_prefix["ipv4Prefix"] + '\",'
                # gcp_ip_address_ranges.append(ip_prefix["ipv4Prefix"])
            if "ipv6Prefix" in ip_prefix:
                googlebot_ip_address_ranges = googlebot_ip_address_ranges + '\"' + ip_prefix["ipv6Prefix"] + '\",'
                # gcp_ip_address_ranges.append(ip_prefix["ipv6Prefix"])

        googlebot_ip_address_ranges = googlebot_ip_address_ranges + "]"

        return googlebot_ip_address_ranges


    def compare_local_and_github_ip_list(local_list, github_list):
        # print(gcp_list, github_list)
        if local_list == github_list:
            return True
        else:
            return False

    # print(get_gcp_ips_list())
    # exit()

    # First create a Github instance:
    # using a personal access token
    github_access_token = environ.get("GITHUB_ACCESS_TOKEN")
    g = Github(github_access_token)

    # Get the repo
    repo = g.get_repo("BrooksCunningham/tfc-verified-bots")

    # Get file in github
    googlebot_ips_file_contents = repo.get_contents("main.auto.tfvars")

    tf_var_formatted_gcp_ip_list = "GOOGLEBOT_IP_LIST = " + get_gcp_ips_list() + "\n\n"
    github_googlebot_ips_file_contents_decoded = googlebot_ips_file_contents.decoded_content.decode()

    googlebot_ip_list_compare = compare_local_and_github_ip_list(tf_var_formatted_gcp_ip_list, github_googlebot_ips_file_contents_decoded)

    if googlebot_ip_list_compare:
        pass
        return "List update: False"
    else:
        repo.update_file(googlebot_ips_file_contents.path
          , "automated GOOGLEBOT_IP_LIST update"
          , tf_var_formatted_gcp_ip_list
          , googlebot_ips_file_contents.sha
          , branch="main")
        return "List update: True"

print(main())
