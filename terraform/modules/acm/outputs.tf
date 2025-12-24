output "certificate_arn" {
  value = aws_acm_certificate_validation.main.certificate_arn
}

output "domain_validation_options" {
  value = aws_acm_certificate.main.domain_validation_options
}
