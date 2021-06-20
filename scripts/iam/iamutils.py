import os

LOCAL_DIR=os.path.dirname(os.path.realpath(__file__))
KEY_DIR=LOCAL_DIR + '/../../config/security'

def find_file(key_file):
    for root, dirs, files in os.walk(KEY_DIR):
        if key_file in files:
            return os.path.join(root, key_file)

def login_service_account(project, sa_name):
    print("Logging in for account: ", sa_name, " for project: ", project)
    key_file = sa_name + '-' + project + '.json'
    file = find_file(key_file)
    print("Found key file: ", file)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = file
