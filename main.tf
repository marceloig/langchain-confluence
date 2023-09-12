data "aws_caller_identity" "this" {}

data "aws_ecr_authorization_token" "token" {}

data "aws_region" "current" {}

locals {
  playlist_name = "spotify-playlist"
}

module "docker_image_spotify_playlist" {
  source = "terraform-aws-modules/lambda/aws//modules/docker-build"

  create_ecr_repo = true
  ecr_repo        = local.playlist_name
  ecr_repo_lifecycle_policy = jsonencode({
    "rules" : [
      {
        "rulePriority" : 1,
        "description" : "Keep only the last 2 images",
        "selection" : {
          "tagStatus" : "any",
          "countType" : "imageCountMoreThan",
          "countNumber" : 2
        },
        "action" : {
          "type" : "expire"
        }
      }
    ]
  })
  image_tag   = "0.18"
  source_path = "pages"
  platform    = "linux/amd64"
}


module "lambda_function_spotify_playlist" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "5.0.0"

  function_name = local.playlist_name
  description   = "My awesome lambda function"

  memory_size    = 1024
  timeout        = 10 # seconds
  create_package = false
  image_uri      = module.docker_image.image_uri
  package_type   = "Image"
  architectures  = ["x86_64"]

  environment_variables = {
    HOST                 = "https://igops.atlassian.net"
    USERNAME             = "igor.oliveira@e-core.com"
    API_TOKEN            = "ATATT3xFfGF00pgC5lhyTkTCGZ_7TwAVl-mAXz3OBlg7-Z-JNiRa_tTY9K2I1jFFBqr4gB6bKr2ZBWaa5lsqhuLtpxM2FMJafatNn-LA5098MyM5gfFSjX1RrWend9AOEb770gc4dwROnKGGzKdrqQt7jhypcZs5BAg2TTseUDqvRi5j7T7XkTY=7323E5E4"
  }
  attach_policy_statements = true
  policy_statements = {
    firehose = {
      effect    = "Allow",
      actions   = ["firehose:PutRecord"],
      resources = [aws_kinesis_firehose_delivery_stream.crawler_confluence_pages_raw.arn]
    }
  }
  create_current_version_allowed_triggers = false
}

module "step_function_spotify" {
  source  = "terraform-aws-modules/step-functions/aws"
  version = "3.1.0"

  name = "sf-spotify"
  definition = templatefile("${path.module}/states.tpl", {
    lambda_function_arn = module.lambda_function_pages.lambda_function_arn
  })

  logging_configuration = {
    include_execution_data = false
    level                  = "ERROR"
  }
  service_integrations = {
    lambda = {
      lambda = [module.lambda_function_pages.lambda_function_arn, "${module.lambda_function_pages.lambda_function_arn}:*"]
    }
  }

  type = "STANDARD"
}

