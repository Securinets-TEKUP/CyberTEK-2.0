variable "region" {
    description = "AWS region for all resources"
    type = string
    default = "us-east-1"
}

variable "instance_type" {
    description = "Instance Type"
    type = string
    default = "t2.large"
  
}

variable "ami_id" {
    description = "Amazon Machine Image ID"
    type = string
    default = "ami-084568db4383264d4" #TODO: add the ami image
}


variable "ssh-public-key-for-ec2" {
  description = "Where to store the public key"
  default     = "cloudVillagePublic.pub"
  type        = string
}

variable "ssh-private-key-for-ec2" {
  description = "Where to store the private key"
  default     = "cloudVillage.pem"
  type        = string
}