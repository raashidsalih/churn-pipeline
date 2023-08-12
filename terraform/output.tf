output "instance_external_ip" {
    description = "External IP address of the instance"
    value       = google_compute_instance.runner-instance.network_interface[0].access_config[0].nat_ip
}

output "private_key" {
  description = "EC2 private key."
  value       = file("ssh-key")
  sensitive   = true
}

output "public_key" {
  description = "EC2 public key."
  value       = file("ssh-key.pub")
}