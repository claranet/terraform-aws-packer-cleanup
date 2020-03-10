variable "name" {
  description = "Name used for Terraform resources."
  default     = "packer-cleanup"
}

variable "lambda_layers" {
  default = []
}
