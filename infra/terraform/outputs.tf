output "vpc_id" {
  description = "AegisFleet VPC ID."
  value       = aws_vpc.aegisfleet.id
}

output "public_subnet_id" {
  description = "AegisFleet public subnet ID."
  value       = aws_subnet.public.id
}

output "instance_id" {
  description = "EC2 instance ID."
  value       = aws_instance.aegisfleet.id
}

output "public_ip" {
  description = "Public IP address of the AegisFleet EC2 instance."
  value       = aws_instance.aegisfleet.public_ip
}

output "ssh_command" {
  description = "SSH command for connecting to the EC2 instance."
  value       = "ssh -i ~/.ssh/aegisfleet_aws ubuntu@${aws_instance.aegisfleet.public_ip}"
}

output "api_url" {
  description = "FastAPI URL."
  value       = "http://${aws_instance.aegisfleet.public_ip}:8000"
}

output "prometheus_url" {
  description = "Prometheus URL."
  value       = "http://${aws_instance.aegisfleet.public_ip}:9090"
}

output "grafana_url" {
  description = "Grafana URL."
  value       = "http://${aws_instance.aegisfleet.public_ip}:3000"
}
