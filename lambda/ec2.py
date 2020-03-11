import boto3

from botocore.exceptions import ClientError


ec2 = boto3.client('ec2')


def delete_key_pair(**kwargs):
    """
    Deletes the specified key pair.

    """

    response = ec2.delete_key_pair(**kwargs)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('ERROR: {}'.format(response))


def delete_security_group(**kwargs):
    """
    Deletes a security group unless it is currently in use.
    Returns True if deleted or False if in use.

    """

    try:
        response = ec2.delete_security_group(**kwargs)
    except ClientError as error:
        response = error.response

    try:
        if response['ResponseMetadata']['HTTPStatusCode'] == 400:
            if response['Error']['Code'] == 'DependencyViolation':
                return False
    except Exception:
        raise Exception('ERROR: {}'.format(response))

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('ERROR: {}'.format(response))

    return True


def describe_instances(**kwargs):
    """
    Describes one or more of your instances.

    """

    paginator = ec2.get_paginator('describe_instances')
    pages = paginator.paginate(**kwargs)
    for page in pages:
        if page['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception('ERROR: {}'.format(page))
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                yield instance

def describe_instances_with_key_names(key_names):
    """
    Describes one or more of your instances whose 'key-name' value matches any item in key_names.

    """
    return describe_instances(
        Filters=[
            {
                'Name': 'key-name',
                'Values': key_names,
            }
        ]
    )

def describe_key_pairs(**kwargs):
    """
    Describes one or more of your key pairs.

    """

    response = ec2.describe_key_pairs(**kwargs)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('ERROR: {}'.format(response))

    return response['KeyPairs']


def describe_security_groups(**kwargs):
    """
    Describes one or more of your security groups.

    """

    response = ec2.describe_security_groups(**kwargs)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('ERROR: {}'.format(response))

    return response['SecurityGroups']


def terminate_instances(**kwargs):
    """
    Shuts down one or more instances.

    """

    response = ec2.terminate_instances(**kwargs)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('ERROR: {}'.format(response))

    return response['TerminatingInstances']
