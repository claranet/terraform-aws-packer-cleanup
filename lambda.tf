module "lambda" {
  source = "github.com/claranet/terraform-aws-lambda?ref=v0.9.1"

  function_name = "${var.name}"
  description   = "Cleans up Packer resources"
  handler       = "main.lambda_handler"
  runtime       = "python3.6"
  timeout       = 300

  source_path = "${path.module}/lambda"

  attach_policy = true
  policy        = "${data.aws_iam_policy_document.lambda.json}"
}

data "aws_iam_policy_document" "lambda" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:DescribeInstances",
      "ec2:DescribeKeyPairs",
      "ec2:DescribeSecurityGroups",
      "ec2:DeleteKeyPair",
      "ec2:DeleteSecurityGroup",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "ec2:TerminateInstances",
    ]

    resources = [
      "*",
    ]

    condition {
      test     = "StringEquals"
      variable = "ec2:ResourceTag/Name"
      values   = ["Packer Builder"]
    }
  }
}
