variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "repo_name" {
  description = "Artifact Registry Docker repository name"
  type        = string
  default     = "fastapi-repo"
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "health-claims-api"
}

variable "docker_image" {
  description = "Full image URI for Cloud Run deployment"
  type        = string
}