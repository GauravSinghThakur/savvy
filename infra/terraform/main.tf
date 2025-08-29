# Terraform scaffold for future infrastructure.
# This file is a placeholder and does not create resources as-is.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  # Region is provided via environment variable or workspace config.
  # Example: AWS_REGION=us-east-1
}

# TODO: Define API Gateway, IAM roles, and service integrations
# module "api_gateway" {
#   source = "./modules/api-gateway"
# }

