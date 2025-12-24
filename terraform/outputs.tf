output "application_url" {
  description = "The DNS name of the Load Balancer"
  value       = "http://${module.alb.dns_name}"
}

output "rds_endpoint" {
  description = "AWS RDS Endpoint (Internal)"
  value       = module.database.db_endpoint
}

output "cdn_url" {
  description = "CloudFront URL (HTTPS)"
  value       = "https://${module.cdn.cloudfront_domain_name}"
}

output "acm_validation_records" {
  description = "DNS Records to add to your Registrar (CNAME)"
  value       = module.acm.domain_validation_options
}
