output "gcp_region" {
  description = "Region set for GCP"
  value       = var.gcp_region
}

output "gcp_zone" {
  description = "Zone set for GCP"
  value       = var.gcp_zone
}

output "instance_external_ip" {
  description = "External IP address of the instance"
  value       = google_compute_instance.runner-instance.network_interface[0].access_config[0].nat_ip
}