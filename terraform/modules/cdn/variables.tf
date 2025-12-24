variable "project_name" {}

variable "alb_dns_name" {}

variable "web_acl_arn" {
  description = "ARN of the WAF Web ACL to attach"
}

variable "domain_name" {
  description = "Custom domain name (e.g., bankedge.click)"
  type        = string
}

variable "acm_certificate_arn" {
  description = "ARN of validated ACM certificate"
  type        = string
}
