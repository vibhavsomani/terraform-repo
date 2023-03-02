terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  access_key = "AKIAWN5LIK446EHCVX3C"
  secret_key = "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"
}