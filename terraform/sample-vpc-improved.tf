terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "aws_region" {
  description = "AWS region where the sample infrastructure will be created."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "allowed_ssh_cidr" {
  description = "Trusted CIDR range allowed to access SSH. Do not use 0.0.0.0/0 for production."
  type        = string

  validation {
    condition     = var.allowed_ssh_cidr != "0.0.0.0/0"
    error_message = "allowed_ssh_cidr must be restricted to a trusted CIDR range, not 0.0.0.0/0."
  }
}

variable "allowed_http_cidr" {
  description = "CIDR range allowed to access HTTP for this sample workload."
  type        = string
  default     = "0.0.0.0/0"
}

variable "ami_id" {
  description = "Approved AMI ID for the EC2 instance."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for the sample web server."
  type        = string
  default     = "t3.micro"
}

variable "environment" {
  description = "Environment name used for tagging and resource context."
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name used for resource naming and tagging."
  type        = string
  default     = "cloudops-ai-assistant"
}

locals {
  # Common tags improve ownership, cost allocation, and operational visibility.
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Owner       = "CloudOps"
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  # Explicit DNS settings make service discovery behavior clear.
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-vpc"
  })
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.public_subnet_cidr

  # Disable automatic public IP assignment by default to reduce accidental exposure.
  map_public_ip_on_launch = false

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-public-subnet"
    Tier = "public"
  })
}

resource "aws_security_group" "web_sg" {
  name        = "${var.project_name}-${var.environment}-web-sg"
  description = "Allow restricted SSH and web traffic for the sample workload"
  vpc_id      = aws_vpc.main.id

  # SSH is restricted to an explicit trusted CIDR instead of the entire internet.
  ingress {
    description = "Allow SSH from trusted administrative network"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  # HTTP remains configurable for the sample; production designs should prefer HTTPS.
  ingress {
    description = "Allow HTTP for sample web traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.allowed_http_cidr]
  }

  # Broad egress is kept for a small sample, but should be narrowed for known production workloads.
  egress {
    description = "Allow outbound traffic for package updates and service calls"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-web-sg"
  })
}

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id

  # In a VPC, security group IDs should be attached with vpc_security_group_ids.
  vpc_security_group_ids = [
    aws_security_group.web_sg.id
  ]

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-web"
    Role = "web"
  })
}
