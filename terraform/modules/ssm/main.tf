resource "aws_ssm_parameter" "database_url" {
  name        = "/${var.project_name}/database_url"
  description = "Database Connection URL for ${var.project_name}"
  type        = "SecureString"
  value       = var.database_url
  overwrite   = true

  tags = {
    Name = "${var.project_name}-database-url"
  }
}

resource "aws_ssm_parameter" "stripe_publishable_key" {
  name        = "/${var.project_name}/stripe_publishable_key"
  description = "Stripe Publishable Key"
  type        = "SecureString"
  value       = var.stripe_publishable_key
  overwrite   = true

  tags = {
    Name = "${var.project_name}-stripe-pk"
  }
}

resource "aws_ssm_parameter" "stripe_secret_key" {
  name        = "/${var.project_name}/stripe_secret_key"
  description = "Stripe Secret Key"
  type        = "SecureString"
  value       = var.stripe_secret_key
  overwrite   = true

  tags = {
    Name = "${var.project_name}-stripe-sk"
  }
}
