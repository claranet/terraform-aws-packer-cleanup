# terraform-aws-packer-cleanup

This module creates an AWS Lambda function that periodically deletes old Packer resources. Packer cleans up after itself if it shuts down cleanly. This module is for when Packer doesn't shut down cleanly.

## Terraform version compatibility

| Module version | Terraform version |
|----------------|-------------------|
| 1.x.x          | 0.12.x            |
| 0.x.x          | 0.11.x            |
