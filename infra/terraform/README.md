# AegisFleet Terraform Baseline

This folder contains the Terraform baseline for the AegisFleet AWS deployment.

## Current scope

This phase creates a simple single-host AWS foundation:

- AWS provider configuration
- Project/environment variables
- Common AWS tags
- Ubuntu EC2 instance
- SSH key pair
- Security group for SSH, FastAPI, Prometheus, and Grafana
- Public IP and service URL outputs

## Not included yet

This phase intentionally does not include:

- RDS
- ALB
- Auto Scaling
- Route 53
- EKS/Kubernetes
- Application deployment

Application bootstrap will be handled later through Ansible.

## Cost note

The default instance type is t3.medium because the future single-host stack is expected to run Docker, FastAPI, PostgreSQL, Prometheus, and Grafana.

Stop or destroy AWS resources when not in use.

## Security note

Before running terraform plan or terraform apply, create a local terraform.tfvars file from terraform.tfvars.example.

Do not commit terraform.tfvars.

Replace open CIDR ranges with your own public IP /32.

Example:

allowed_admin_cidr_blocks = ["203.0.113.10/32"]

For your local machine, use your current public IP followed by /32.

## Safe workflow

Run these commands from infra/terraform:

terraform fmt -recursive
terraform init
terraform validate
terraform plan

Do not run terraform apply until the plan has been reviewed.
