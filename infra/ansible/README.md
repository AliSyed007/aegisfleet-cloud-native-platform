# AegisFleet Ansible Bootstrap

This folder contains the Ansible bootstrap workflow for the AegisFleet EC2 host.

## Current scope

The playbook prepares a single Ubuntu EC2 server by:

- installing base packages
- installing Docker
- installing Docker Compose v2
- enabling Docker service
- creating the app directory
- cloning the AegisFleet repository
- creating .env from .env.example
- starting the Docker Compose stack
- verifying the FastAPI health endpoint locally

## Not included yet

This phase does not include:

- Kubernetes
- RDS bootstrap
- TLS/SSL
- domain setup
- advanced hardening
- blue/green deployment

## Inventory workflow

Copy the example inventory after Terraform creates the EC2 instance:

cp inventory.example.ini inventory.ini

Then replace:

REPLACE_WITH_EC2_PUBLIC_IP

with the public IP from Terraform output.

The real inventory.ini file is ignored by Git.

## Run workflow

From this folder:

ansible-playbook bootstrap.yml

## Notes

The playbook assumes:

- Ubuntu EC2 host
- SSH user is ubuntu
- SSH private key is ~/.ssh/aegisfleet_aws
- repository is reachable from the EC2 host
