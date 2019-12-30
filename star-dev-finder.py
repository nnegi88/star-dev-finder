import requests
from collections import OrderedDict
from operator import itemgetter

base_url = "https://api.github.com"

# username and password are must as some members in organization may have their visibility as private
username = "" # enter your github username here
password = "" # enter your github password here
organization_name = "" # enter the name of organization
  
org_member_url = base_url+"/orgs/"+organization_name+"/members"

r = requests.get(url = org_member_url, auth = requests.auth.HTTPBasicAuth(username, password)) 

members_response = r.json()

members_count = len(members_response)

print("Total number of members in %s: %s"%(organization_name, members_count))
print("Loading... This may take a while depending upon the number of members in the organization\n")

member_dictionary = {} 

for member in members_response:
    member_name = member['login']
    user_repos_url = base_url+"/users/"+member_name+"/repos?per_page=1000" # as default limit per page is 30
    r = requests.get(url = user_repos_url, auth = requests.auth.HTTPBasicAuth(username, password)) 
    repos_response = r.json()
    repos_response_unforked = filter(lambda x: not x['fork'], repos_response) # filtering forked repos
    repos_count = len(repos_response_unforked)
    member_dictionary[member_name] = repos_count

sorted_members_dict = OrderedDict(sorted(member_dictionary.items(), key=itemgetter(1)))

print("Members repo count in ascending order are below:\n")
for member_name, repos_count in sorted_members_dict.items():
    print("%s - %s"%(member_name,repos_count))

print("\n%s is the star developer of the organization %s"%(member_name, organization_name))
