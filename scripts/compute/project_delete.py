#!/usr/bin/python3.8

"""
Script to clean up project after testing
Will remove all disks and VMs!
"""

import sys
import os
import argparse 
import googleapiclient.discovery
import compute_utils as cu

local_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, local_file_path + '/../iam/')
import iamutils as iam


def main(project, zone, service_account):
    iam.login_service_account(project, service_account)
    compute = googleapiclient.discovery.build('compute', 'v1')
    instances = cu.list_instances(compute, project, zone)
    if not instances == None:
        for vm in instances['items']:
            cu.delete_instance(compute, project, vm['zone'].split('/')[-1], vm['name'])
    disks = cu.list_disks(compute, project, zone)
    if not disks == None:
        for disk in disks:
            cu.delete_disk(compute, project, disk['zone'].split('/')[-1], disk['name'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Delete all vms and disks in a project',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project_id', default='composite-jetty-193607', help='Project ID to clean up')
    parser.add_argument('--zone', default='europe-west2-b', help='Project zone to clean up')
    parser.add_argument('--service_account', default='26533232462-compute', help='Project SA to use')
    args = parser.parse_args()
    main(args.project_id, args.zone, args.service_account)
