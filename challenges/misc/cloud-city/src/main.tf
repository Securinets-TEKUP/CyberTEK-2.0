provider "aws" {
    region = var.region  
}
provider "random" {}


resource "aws_vpc" "main-vpc" {
  cidr_block           = "10.10.0.0/16"
  enable_dns_hostnames = true
}

#Internet Gateway
resource "aws_internet_gateway" "main-internet-gateway" {
  vpc_id = aws_vpc.main-vpc.id

}

#Public Subnets
resource "aws_subnet" "main-public-subnet-1" {
  availability_zone = "${var.region}a"
  cidr_block        = "10.10.10.0/24"
  vpc_id            = aws_vpc.main-vpc.id

}

resource "aws_subnet" "main-public-subnet-2" {
  availability_zone = "${var.region}b"
  cidr_block        = "10.10.20.0/24"
  vpc_id            = aws_vpc.main-vpc.id

}

#Public Subnet Routing Table
resource "aws_route_table" "main-public-subnet-route-table" {
  vpc_id = aws_vpc.main-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main-internet-gateway.id
  }

}
#Public Subnets Routing Associations
resource "aws_route_table_association" "main-public-subnet-1-route-association" {
  subnet_id      = aws_subnet.main-public-subnet-1.id
  route_table_id = aws_route_table.main-public-subnet-route-table.id
}

resource "aws_route_table_association" "main-public-subnet-2-route-association" {
  subnet_id      = aws_subnet.main-public-subnet-2.id
  route_table_id = aws_route_table.main-public-subnet-route-table.id
}


locals {
  # Unique suffix for bucket name
  s3_bucket_suffix = random_id.server.hex

  # Absolute path to the dir containing your site
  website_dir   = "${path.module}/assets/Horizontal_Website"
  # Recursively list all files under that dir
  website_files = fileset(local.website_dir, "**")
}

# ——————————————————————————————————————————————
# 1) Create the bucket (no inline ACLs or website blocks here)
# ——————————————————————————————————————————————
resource "aws_s3_bucket" "cloud_city_data" {
  bucket        = "cloud-city-${local.s3_bucket_suffix}"
  force_destroy = true

  tags = {
    Name = "cloud-city-${local.s3_bucket_suffix}"
  }
}

# ——————————————————————————————————————————————
# 2) Enable versioning via dedicated resource
# ——————————————————————————————————————————————
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.cloud_city_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

# ——————————————————————————————————————————————
# 3) Configure static-website hosting
# ——————————————————————————————————————————————
resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.cloud_city_data.id

  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "error.html"
  }
}

# ——————————————————————————————————————————————
# 4) Allow public access via bucket policy (no ACLs at all)
# ——————————————————————————————————————————————
resource "aws_s3_bucket_public_access_block" "public_block" {
  bucket                  = aws_s3_bucket.cloud_city_data.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

data "aws_iam_policy_document" "public_read" {
  statement {
    effect    = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.cloud_city_data.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.cloud_city_data.id
  policy = data.aws_iam_policy_document.public_read.json
}

# ——————————————————————————————————————————————
# 5) Upload every file under assets/Horizontal_Website
# ——————————————————————————————————————————————
resource "aws_s3_object" "website_files" {
  for_each = toset(local.website_files)

  bucket = aws_s3_bucket.cloud_city_data.id
  key    = each.value
  source = "${local.website_dir}/${each.value}"

  tags = {
    Name = "cloud-city-${local.s3_bucket_suffix}"
  }
}

# ——————————————————————————————————————————————
# 6) Output your website endpoint
# ——————————————————————————————————————————————
output "website_endpoint" {
  value = aws_s3_bucket.cloud_city_data.website_endpoint
}



resource "random_id" "server" {
  byte_length = 8
}

resource "aws_iam_user" "loki" {
    name = "loki"
}


resource "aws_iam_access_key" "loki_key" {
  user = aws_iam_user.loki.name
}

resource "aws_security_group" "ec2-http-sg" {
  name        = "ec2-http-sg"
  description = "Allow HTTP traffic"
  vpc_id      = aws_vpc.main-vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
      Name = "ec2-http-sg"
    }
}


resource "aws_security_group" "ec2_ssh_security_group" {
    name = "ec2-ssh-sg"
    description = "Allow ssh traffic to ec2 instance"
    vpc_id = aws_vpc.main-vpc.id   


    ingress {
        from_port = 22
        to_port = 22
        protocol =  "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = -1
        cidr_blocks = ["0.0.0.0/0"]
    }
 
    tags = {
      Name = "ec2-ssh-sg"
    }

}

resource "aws_key_pair" "ec2-key-pair" {
  key_name   = "ec2-key-pair-${random_id.server.hex}"
  public_key = file(var.ssh-public-key-for-ec2)
}

# Look up the existing instance
# 1) Look up your existing EC2 instance
data "aws_instance" "reverse_proxy" {
  instance_id = "i-0c45ac9de0da859e5"
}

# 2) (Re)create your IAM instance profile
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2-instance-profile-${random_id.server.hex}"
  role = aws_iam_role.ec2_volumes_management.name
}

# 3) Associate that profile with the existing instance
resource "aws_iam_instance_profile_association" "attach_profile" {
  instance_id          = data.aws_instance.reverse_proxy.id
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
}


data "aws_iam_policy_document" "ec2_lambda_access" {
  statement {
    sid     = "AllowListAllLambdas"
    effect  = "Allow"
    actions = [
      "lambda:ListFunctions",
    ]
    # ListFunctions must be Resource="*"
    resources = ["*"]
  }

  statement {
    sid     = "AllowInvokeVulnLambda"
    effect  = "Allow"
    actions = [
      "lambda:InvokeFunction",
    ]
    # scope down to your specific function
    resources = [
      aws_lambda_function.upload_to_s3_bucket.arn
    ]
  }
}


# resource "aws_instance" "reverse_proxy_server" {
#   ami                         = var.ami_id
#   instance_type               = var.instance_type
#   iam_instance_profile        = aws_iam_instance_profile.ec2_instance_profile.name
#   vpc_security_group_ids      = [ aws_security_group.ec2_ssh_security_group.id, aws_security_group.ec2-http-sg.id ]
#   key_name                    = aws_key_pair.ec2-key-pair.key_name
#   subnet_id                   = aws_subnet.main-public-subnet-1.id
#   associate_public_ip_address = true

#   tags = {
#     Name = "reverse_proxy_server_${random_id.server.hex}"
#   }
# }


resource "aws_secretsmanager_secret" "ssh_key" {
  name        = "ssh-keys-for-user-itachi"        # whatever logical name you like
  description = "ssh key for the rev proxy server"
}

resource "aws_secretsmanager_secret_version" "ssh_secret_value" {
  secret_id     = aws_secretsmanager_secret.my_secret.id
  secret_string = file("${path.module}/cloudVillage.pem")
}




data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_role" "iam_for_lambda" {
  name               = "upload-to-s3"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_iam_role_policy_attachment" "basic_exec" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}



data "aws_iam_policy_document" "lambda_s3_secrets" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject"]

    resources = [
      "arn:aws:s3:::skyfall2025",
      "arn:aws:s3:::skyfall2025/*",
    ]

  }


  statement {
    sid     = "AllowSecretsManagerRead"
    effect  = "Allow"
    actions = [
      "secretsmanager:DescribeSecret",
      "secretsmanager:GetSecretValue",
      "secretsmanager:ListSecretVersionIds",
    ]
    resources = [
      aws_secretsmanager_secret.ssh_key.arn,
    ]
  }
}

resource "aws_iam_role_policy" "lambda_s3_secrets" {
  name   = "lambda_s3_and_secrets_policy"
  role   = aws_iam_role.iam_for_lambda.id
  policy = data.aws_iam_policy_document.lambda_s3_secrets.json
}

data "archive_file" "lambda_function" {
  type        = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "upload_to_s3_bucket" {
  filename         = data.archive_file.lambda_function.output_path
  function_name    = "upload-to-s3-bucket"
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_function.output_base64sha256
  runtime          = "python3.11"

  environment {
    variables = {
      BUCKET_NAME = "skyfall2025"
      SECRET_MESSAGE = "bm90IGZpbnNoZWQgeWV0LCB0aGlzIGlzIG9ubHkgdGhlIGZpcnN0IHBhcnQgb2YgdGhlIGNoYWxsZW5nZSBrZWVwIGdvaW5n"
    }
  }
}

resource "aws_iam_role" "ec2_volumes_management" {
  name = "ec2_volumes_management"

    assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}



resource "aws_iam_role_policy" "ec2_lambda_policy" {
  name   = "ec2-access-lambda"
  role   = aws_iam_role.ec2_volumes_management.id
  policy = data.aws_iam_policy_document.ec2_lambda_access.json
}