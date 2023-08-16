variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-c"
}

variable "instance_type" {
  description = "Instance type for GCP VM"
  type        = string
  default     = "e2-standard-2"
}

variable "instance_zone" {
  description = "GCP VM zone"
  type        = string
  default     = "us-central1-c"
}