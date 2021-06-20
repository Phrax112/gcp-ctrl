# Cloud Control

A Python repository for controlling a Google Cloud Project

## Directory Structure
```
── config
│   ├── security
│   └── vm
└── scripts
    ├── compute
    ├── iam
    └── startup_scripts
```

## Directory Breakdown

### config

A folder containing all files which contain data relevant to running and maintaining the Cloud project. All items should be non-executable and are broadly divided between config items related to security and Virtual Machine config files.

#### security
* This config subfolder should primarily be empty and all components when used locally should be listed in your .gitignore file to ensure they are not accidentally committed to the repository.
* This folder is where all security information required by tthe cloud project should be contained.
* Items such as service account keys and ssh certificates will be placed in this folder by the build pipelines

#### vm
* This folder is for VM configuration files. 
* These are files which describe the attributes of VMs which are used in this project
* These attributes can include the size of the machine, what disks it should have, it's location etc...

### scripts

All executable scripts for running the project. Used to deploy VMs, manage accounts and firewalls as well as start applications.

#### compute
* Containing all scripts pertaining to the management of Virtual Machines and Google Compute Engine broadly
* These are scripts to be run on an infrastructure host (i.e. your computer or anywhere with permissions to manage the project)
* They require an account to be logged in or a service acount key to be available for login

#### iam
* Any script relevant to managing the identity access management roles of the project
* These are for creating, deleting and rotating service account keys
* Also for managing user accounts securely

#### startup_scripts
* These are scripts which are used to initialise a VM after the hardware has been set up by the compute script
* They start any applications which will run on the VM and perform health checks to ensure they are working properly
* Generally written in a shell language or Python as appropriate
