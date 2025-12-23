output "database_url_arn" {
  value = aws_ssm_parameter.database_url.arn
}

output "database_url_name" {
  value = aws_ssm_parameter.database_url.name
}
