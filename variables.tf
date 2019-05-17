variable "name" {
  description = "Name used for Terraform resources."
  type        = "string"
  default     = "packer-cleanup"
}

variable "lambda_layers" {
  default = []
}
