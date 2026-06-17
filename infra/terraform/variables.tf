variable "aws_region" {
  description = "AWS region for the AegisFleet baseline infrastructure."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used for AWS resource naming."
  type        = string
  default     = "aegisfleet"
}

variable "environment" {
  description = "Environment name for this deployment."
  type        = string
  default     = "dev"
}

variable "instance_type" {
  description = "EC2 instance type for the single-host AegisFleet portfolio deployment."
  type        = string
  default     = "t3.medium"
}

variable "ssh_public_key" {
  description = "Public SSH key content used to create the EC2 key pair."
  type        = string
  sensitive   = true
}

variable "allowed_admin_cidr_blocks" {
  description = "CIDR blocks allowed for SSH, Prometheus, and Grafana. Replace with your public IP /32 before apply."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_api_cidr_blocks" {
  description = "CIDR blocks allowed to access the FastAPI service."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "vpc_cidr_block" {
  description = "CIDR block for the AegisFleet VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidr_block" {
  description = "CIDR block for the public subnet."
  type        = string
  default     = "10.20.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone for the public subnet."
  type        = string
  default     = "eu-central-1a"
}
