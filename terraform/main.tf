terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.51.0"
    }
  }

  required_version = ">= 1.2.0"
}

provider "google" {
  credentials = file("customer-churn-pipeline-5f468f8118ff.json")

  project = "customer-churn-pipeline"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_compute_instance" "runner-instance" {
  name                    = "runner-instance"
  machine_type            = "e2-standard-2"
  zone                    = "us-central1-a"
  tags = ["runner-instance"]
  metadata_startup_script = file("setup.sh")

  metadata = {
    ssh-keys = "admin:${file("ssh-key.pub")}"
  }

  # Specify the boot disk image
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 20
    }
  }

  # Specify the network interface
  network_interface {
    network = "default"

    # Assign an ephemeral external IP address
    access_config {}
  }
}

resource "google_compute_firewall" "ssh-rule" {
  name    = "ssh-rule"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]

  target_tags   = ["runner-instance"]
}

resource "google_compute_firewall" "docker-firewall" {
  name    = "docker-firewall"
  network = "default"

  # Allow ingress traffic
  direction = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "4000", "3000"]
  }

  source_ranges = ["0.0.0.0/0"]

  # Apply the rule to the compute instance
  target_tags = ["runner-instance"]
}