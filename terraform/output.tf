output "instance_external_ip" {
    description = "External IP address of the instance"
    value       = google_compute_instance.runner-instance.network_interface[0].access_config[0].nat_ip
}
