resource "aws_s3_bucket" "service_logs" {
  bucket = "cloud-service-logs-${random_id.suffix.hex}"

  force_destroy = true
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.service_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}
