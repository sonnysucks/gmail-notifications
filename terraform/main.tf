# SnapStudio Basic Cloudflare Deployment
# Simplified version that works with basic Zone API token

terraform {
  required_version = ">= 1.0"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

# Configure Cloudflare provider
provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# Variables
variable "domain" {
  description = "Domain name for SnapStudio"
  type        = string
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type        = string
  sensitive   = true
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID"
  type        = string
}

# Cloudflare Zone
data "cloudflare_zone" "main" {
  name = var.domain
}

# Cloudflare D1 Database (this worked!)
resource "cloudflare_d1_database" "snapstudio" {
  account_id = var.cloudflare_account_id
  name       = "snapstudio-db"
}

# Simple DNS Records (pointing to a placeholder for now)
resource "cloudflare_record" "snapstudio" {
  zone_id = data.cloudflare_zone.main.id
  name    = var.domain
  content = "192.0.2.1"  # Placeholder IP - will update later
  type    = "A"
  ttl     = 1
}

resource "cloudflare_record" "snapstudio_www" {
  zone_id = data.cloudflare_zone.main.id
  name    = "www"
  content = "192.0.2.1"  # Placeholder IP - will update later
  type    = "A"
  ttl     = 1
}

# Outputs
output "domain_url" {
  value = "https://${var.domain}"
}

output "database_id" {
  value = cloudflare_d1_database.snapstudio.id
}

output "next_steps" {
  value = "1. Enable R2 in Cloudflare Dashboard 2. Update DNS records 3. Deploy Worker manually"
}
