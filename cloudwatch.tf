resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${var.name}-schedule"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "schedule" {
  target_id = "${var.name}-schedule"
  rule      = "${aws_cloudwatch_event_rule.schedule.name}"
  arn       = "${module.lambda.function_arn}"
}

resource "aws_lambda_permission" "schedule" {
  statement_id  = "${var.name}-schedule"
  action        = "lambda:InvokeFunction"
  function_name = "${module.lambda.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.schedule.arn}"
}
