
resource "aws_cloudwatch_event_rule" "schedule_rule" {
  name        = "movielens-scheduled-rule"
  description = "Scheduled rule to trigger moviele ns Lambda function"

  schedule_expression = "cron(0 12 * * ? *)"  # Change to your desired schedule

  tags = {
    Environment = "Production"
  }
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.schedule_rule.name
  arn       = aws_lambda_function.lambda-source-raw.arn
  target_id = "my-lambda-target"
}