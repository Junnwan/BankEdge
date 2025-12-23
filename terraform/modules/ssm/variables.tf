variable "project_name" {}

variable "database_url" {
  description = "Full PostgreSQL connection string"
  sensitive   = true
}

variable "stripe_publishable_key" {
  description = "Stripe Publishable Key"
  sensitive   = true
}

variable "stripe_secret_key" {
  description = "Stripe Secret Key"
  sensitive   = true
}
