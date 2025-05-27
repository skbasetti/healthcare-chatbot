provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = var.repo_name
  format        = "DOCKER"

  lifecycle {
    prevent_destroy = false
    ignore_changes  = [repository_id] # optional safeguard
  }
}

resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloudrun-fastapi"
  display_name = "Cloud Run FastAPI Service Account"
}

resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = format("serviceAccount:%s", google_service_account.cloud_run_sa.email)
}

resource "google_cloud_run_service" "fastapi_service" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.docker_image
        ports {
          container_port = 8080
        }
      }
      service_account_name = google_service_account.cloud_run_sa.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}

terraform {
  backend "gcs" {
    bucket = "terraform-state-claims-queries"
    prefix = "health-bot/terraform.tfstate"
  }
}
