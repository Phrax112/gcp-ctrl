#!/usr/bin/python3.8

"""
delete  Deletes the specified firewall.
get     Returns the specified firewall.
insert	Creates a firewall rule in the specified project using the data included in the request.
list	Retrieves the list of firewall rules available to the specified project.
update	Updates the specified firewall rule with the data included in the request.
"""

import googleapiclient.discovery
import iamutils as iam

def readConfig(config_file):
    print("Reading config from file: ", config_file)
    with open(config_file, 'r') as file:
        config=file.read()
    firewall_body=json.loads(config)
    return firewall_body

def listFirewallRules(compute, project):
    request = compute.firewalls().list(project=project)
    while request is not None:
        response = request.execute()
        for firewall in response['items']:
            print(firewall)
        request = compute.firewalls().list_next(previous_request=request, previous_response=response)

def insertFirewallRule(compute, project, config_file):
    firewall_body = readConfig(config_file)
    print("Inserting firewall rule: ", firewall_body)
    request = compute.firewalls().insert(project=project, body=firewall_body)
    response = request.execute()
    print(response)
    
def getFirewallRule(compute, project, config_file):
    firewall_body = readConfig(config_file)
    print("Getting firewall rule: ", firewall_body['name'])
    request = compute.firewalls().get(project=project, firewall=firewall_body['name'])
    response = request.execute()
    print(response)

def deleteFirewallRule(compute, project, config_file):
    firewall_body = readConfig(config_file)
    print("Deleting firewall rule: ", firewall_body['name'])
    request = compute.firewalls().delete(project=project, firewall=firewall_body['name'])
    response = request.execute()
    print(response)

def updateFirewallRule(compute, project, config_file):
    firewall_body = readConfig(config_file)
    print("Updating firewall rule: ", firewall_body)
    request = compute.firewalls().update(project=project, firewall=firewall_body['name'], body=firewall_body)
    response = request.execute()
    print(response)

def main(project, action, config_file, service_account):
    print("Running firewall ", action," for project: ", project)
    iam.login_service_account(project, service_account)
    compute = googleapiclient.discovery.build('compute', 'v1')
    if action == "list":
        listFirewallRules(compute, project)
    elif action == "insert":
        insertFirewallRule(compute, project, config_file)
    elif action == "get":
        getFirewallRule(compute, project)
    elif action == "delete":
        deleteFirewallRule(compute, project)
    elif action == "update":
        updateFirewallRule(compute, project)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Create a firewall rule based on a config file',
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project_id', default='composite-jetty-193607', help='Your Google Cloud project ID.')
    parser.add_argument('--action', default='list', help='Action to take (see comments in file for list of options)')
    parser.add_argument('--config_file', default='../../config/security/firewall/test.json', help='Firewall config')
    args = parser.parse_args()
    main(args.project_id, action, args.config_file)

