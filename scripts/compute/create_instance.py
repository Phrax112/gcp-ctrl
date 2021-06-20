#!/usr/bin/python3.8

"""
Script to create a compute instance based on three variables
--project_id
--config_file
--startup_script
"""

import argparse
import os
import json
import compute_utils as cu
import googleapiclient.discovery
import sys

local_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, local_file_path + '/../iam/')
import iamutils as iam

def create_instance(compute, project, startup_script, vm_config):
    # Get the image specified.
    image_response = compute.images().getFromFamily(
        project=vm_config['image_project'], family=vm_config['image_family']).execute()
    source_disk_image = image_response['selfLink']
    # Configure the machine
    machine_type = ("zones/%s/machineTypes/" + vm_config['machine_type']) % vm_config['zone']
    startup_script = open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../startup_scripts", startup_script), 'r').read()

    ssh_keys = open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../../config/security/"+ vm_config["ssh_keys"]), 'r').read()
    
    config = {
        'name': vm_config['name'],
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT', 'natIP': vm_config["natIP"]}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/logging.write',
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/compute',
                'https://www.googleapis.com/auth/source.full_control'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, {
                'key': 'ssh-keys',
                'value': ssh_keys
            }
            ]
        }
    }
    return compute.instances().insert(
        project=project,
        zone=vm_config['zone'],
        body=config).execute()

def create_attach_disks(compute, project, config):
    for disk in config['disks']:
        if not cu.check_disk_exists(compute, project, config['zone'], disk):
            cu.create_disk(compute, project, config['zone'], disk, config['disks'][disk]['size'])
        else:
            print("Disk already created: ", disk)
    for disk in config['disks']:
        cu.attach_disk(compute, project, config['zone'], config['name'], disk, config['disks'][disk])
    return None

def main(project, startup_script, config_file):
    print('Reading config from file: ', config_file)
    with open(config_file, 'r') as file:
        config=file.read()
    config=json.loads(config)
    print(config)
    iam.login_service_account(project, config['service_account'])
    compute = googleapiclient.discovery.build('compute', 'v1')
    cu.delete_instance(compute, project, config['zone'], config['name'])
    print('Creating instance.')
    operation = create_instance(compute, project, startup_script, config)
    cu.wait_for_operation(compute, project, config['zone'], operation['name'])
    create_attach_disks(compute, project, config)
    print("Instance created in project %s and zone %s:" % (project, config['zone']))
    print("It will take a minute or two for the instance to complete it's startup script.")
    instances = cu.list_instances(compute, project, config['zone'])
    print(instances)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Create a compute instance based on a config file',
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project_id', default='composite-jetty-193607', help='Your Google Cloud project ID.')
    parser.add_argument('--startup_script', 
        default='../startup_scripts/test.sh', 
        help='The path to the startup script')
    parser.add_argument('--config_file', default='../../config/vm/test.json', help='VM config')
    args = parser.parse_args()
    main(args.project_id, args.startup_script, args.config_file)
