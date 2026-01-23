
import boto3

ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

def get_instances(action, tag_key, tag_value):
    instances = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{tag_key}', 'Values': [tag_value]},
            {'Name': 'instance-state-name', 'Values': ['running' if action == 'stop' else 'stopped']}])
    instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
    return instance_ids

def get_keys_by_tag(tag_key, tag_value):
    instances = ec2.describe_instances(
        Filters=[
            {'Name': f'tag:{tag_key}', 'Values': [tag_value]}])
    key_names = [instance['KeyName'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
    if len(key_names) == 0:
        return []
    key_names = list(set(key_names))  # Remove duplicates
    key_ids = get_key_ids_from_key_names(key_names)
    return key_ids

def get_key_ids_from_key_names(key_names):
    keys = ec2.describe_key_pairs(
        Filters=[
            {'Name': 'key-name', 'Values': key_names}])
    if len(keys['KeyPairs']) == 0:
        return None
    return [key['KeyPairId'] for key in keys['KeyPairs']]

def get_private_key_from_ssm(key_names):
    private_keys = []
    for key_name in key_names:
        parameter_name = f'/ec2/keypair/{key_name}'
        try:
            response = ssm.get_parameter(
                Name=parameter_name,
                WithDecryption=True
            )
        except ssm.exceptions.ParameterNotFound:
            print(f"Parameter {parameter_name} not found in SSM.")
            continue
        private_key = response['Parameter']['Value']
        private_keys.append(private_key)
    return private_keys