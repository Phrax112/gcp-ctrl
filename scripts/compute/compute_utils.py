import time

# https://cloud.google.com/compute/docs/reference/rest/v1/instances/delete
def delete_instance(compute, project, zone, name):
    print("Removing instance ", name," if it exists in project: ", project)
    try:
        operation = compute.instances().delete(
            project=project,
            zone=zone,
            instance=name).execute()
        wait_for_operation(compute, project, zone, operation['name'])
        return operation
    except:
        print("Instance could not be deleted")

# https://cloud.google.com/compute/docs/reference/rest/v1/zoneOperations/get
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        try:
            result = compute.zoneOperations().get(
                project=project,
                zone=zone,
                operation=operation).execute()
        except:
            print("Couldn't find operation... continuing")
            return True
        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(5)

# https://cloud.google.com/compute/docs/reference/rest/v1/instances/list
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result if 'items' in result else None

def list_disks(compute, project, zone):
    request = compute.disks().list(project=project, zone=zone)
    res = []
    while request is not None:
        response = request.execute()
        for disk in response['items']:
            res.append(disk)
        request = compute.disks().list_next(previous_request=request, previous_response=response)
    return res

# https://cloud.google.com/compute/docs/reference/rest/v1/disks/insert
def create_disk(compute, project, zone, name, size):
    print("Creating disk: ", name, size, " in zone: ", zone," in project: ", project)
    disk_body = {
        'name': name,
        'sizeGb': size
        }
    request = compute.disks().insert(project=project, zone=zone, body=disk_body)
    try:
        res = request.execute()
        return res
    except:
        print("Failed to create disk")
        return None

# https://cloud.google.com/compute/docs/reference/rest/v1/disks/delete
def delete_disk(compute, project, zone, name):
    print("Deleting disk: ", name, " in zone: ", zone," in project: ", project)
    request = compute.disks().delete(project=project, zone=zone, disk=name)
    try: 
        res = request.execute()
        return res
    except:
        print("Failed to delete disk")
        return None
   
# https://cloud.google.com/compute/docs/reference/rest/v1/disks/get
def check_disk_exists(compute, project, zone, name):
    request = compute.disks().get(project=project, zone=zone, disk=name)
    try:
        res = request.execute()
    except:
        res = {}
    return True if 'name' in res else False

# https://cloud.google.com/compute/docs/reference/rest/v1/instances/attachDisk
def attach_disk(compute, project, zone, instance, disk, config):
    print("attaching disk: ", disk, "to instance: ", instance)
    url = 'projects/' + project + '/zones/' + zone + '/disks/' + disk
    body = { 'name': disk, 'mode': config['mode'], 'deviceName': config['deviceName'], 'source': url }
    request = compute.instances().attachDisk(project=project, zone=zone, instance=instance, body=body)
    try:
        res = request.execute()
        return res
    except:
        print("Failed to attach disk")
        return None
