import packer


def lambda_handler(event, context):
    packer.cleanup()
