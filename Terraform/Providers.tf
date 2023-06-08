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
}
terraform {
    backend "s3" {
        bucket = "indusvalley-source-config"
        #dynamodb_table = "terraform-state-lock-db"
        key = "secure-ingest-tf/terraform-state/tfstate.json"
        region = "us-east-1"
    }
}