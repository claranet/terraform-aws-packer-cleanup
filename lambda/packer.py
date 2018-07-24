from __future__ import print_function

import calendar
import datetime
import ec2
import time


def cleanup():
    """
    Cleans up old Packer resources. They can be left behind
    when Packer does not shut down cleanly.

    """

    # Terminate old Packer EC2 instances.
    instance_ids = []
    for instance in get_old_packer_instances():
        instance_ids.append(instance['InstanceId'])
    if instance_ids:
        print('Terminating old Packer EC2 instances: {}'.format(
            ', '.join(instance_ids)
        ))
        ec2.terminate_instances(
            InstanceIds=instance_ids,
        )

    # Delete Packer key pairs that aren't in use by any EC2 instances.
    for key_name in get_old_packer_keys():
        print('Deleting old Packer key pair {}'.format(key_name))
        ec2.delete_key_pair(
            KeyName=key_name,
        )

    # Delete all Packer security groups.
    # If a security group is in use, it can't be deleted.
    for security_group in get_packer_security_groups():
        security_group_id = security_group['GroupId']
        print('Deleting Packer security group {}'.format(security_group_id))
        deleted = ec2.delete_security_group(
            GroupId=security_group_id,
        )
        if not deleted:
            print('Security group is currently in use, not deleted')


def get_old_packer_instances():
    """
    Returns Packer EC2 instances older than 6 hours.

    """

    oldest_launch_dt = datetime.datetime.now() - datetime.timedelta(hours=6)
    oldest_launch_ts = calendar.timegm(oldest_launch_dt.timetuple())

    instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'Packer Builder',
                ]
            }
        ]
    )
    for instance in instances:
        instance_launch_ts = time.mktime(instance['LaunchTime'].timetuple())
        if instance_launch_ts < oldest_launch_ts:
            yield instance


def get_old_packer_keys():
    """
    Returns Packer EC2 key pairs that are not in use.

    """

    # Get all Packer keys.
    packer_keys = set()
    for key in ec2.describe_key_pairs():
        key_name = key['KeyName']
        if key_name.startswith('packer_'):
            packer_keys.add(key_name)

    # Exclude keys used by EC2 instances.
    instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'key-name',
                'Values': list(packer_keys),
            }
        ]
    )
    for instance in instances:
        key_name = instance['KeyName']
        packer_keys.discard(key_name)

    return list(packer_keys)


def get_packer_security_groups():
    """
    Returns Packer security groups.

    """

    return ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'description',
                'Values': ['Temporary group for Packer'],
            },
        ],
    )
