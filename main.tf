variable "region" {
  default = "eu-central-1"
}

variable "role" {
  default= "arn:aws:iam::805431852690:role/qls-624354-dd299561b11af006-PlayerRole-1WLHP15R0BHNM"
}


provider "aws" {
  region = "${var.region}"
}

resource "aws_lambda_function" "kinesis" {
  filename = "kinesis.zip"
  function_name = "kinesis"
  role = "${var.role}"
  handler = "kinesis.handler"
  runtime = "python2.7"
  source_code_hash = "${base64sha256(file("kinesis.zip"))}"
}

# resource "aws_lambda_function" "publish" {
#   filename = "publish.zip"
#   function_name = "publish"
#   role = "${var.role}"
#   handler = "publish.handler"
#   runtime = "python2.7"
# }

resource "aws_kinesis_stream" "default" {
  name = "area51"
  shard_count = 1
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
    batch_size = 100
    event_source_arn = "${aws_kinesis_stream.default.arn}"
    enabled = true
    function_name = "${aws_lambda_function.kinesis.arn}"
    starting_position = "LATEST"
}

# resource "aws_lambda_function" "s3" {
#   filename = "s3.zip"
#   function_name = "s3"
#   role = "${var.role}"
#   handler = "s3.handler"
#   runtime = "python2.7"
# }

# resource "aws_dynamodb_table" "pending" {
#   name = "pending"
#   read_capacity = 5
#   write_capacity = 5
#   hash_key = "Id"
#   range_key = "PartNumber"

#   attribute {
#     name = "Id"
#     type = "S"
#   }

#   attribute {
#     name = "PartNumber"
#     type ="N"
#   }
# }
