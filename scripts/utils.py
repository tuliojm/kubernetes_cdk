
import boto3

ec2 = boto3.client('ec2')
def get_instances(action, tag_key, tag_value):
    instances = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
            {'Name': 'instance-state-name', 'Values': ['running' if action == 'stop' else 'stopped']}])
    instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
    return instance_ids