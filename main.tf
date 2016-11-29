variable "region" { default = "eu-central-1" }
variable "role" { default= "arn:aws:iam::805431852690:role/qls-624354-dd299561b11af006-PlayerRole-1WLHP15R0BHNM"}

provider "aws" {
  region = "${var.region}"
}

resource "aws_lambda_function" "kinesis" {
  filename = "kinesis.zip"
  function_name = "kinesis"
  role = "${var.role}"
  handler = "handler"
  runtime = "python2.7"
}
