import boto3
import argparse
from utils import get_instances

ec2 = boto3.client('ec2')

def main(action, tag_key, tag_value):
    instance_ids = get_instances(tag_key, tag_value, action)
    if len(instance_ids) == 0:
        print(f"No instances found with tag {tag_key}={tag_value} in the appropriate state for action '{action}'.")
        return
    
    if action == 'stop':
        response = ec2.stop_instances(InstanceIds=instance_ids)
    elif action == 'start':
        response = ec2.start_instances(InstanceIds=instance_ids)
        # Wait instances to be running
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=instance_ids)
        # Describe instances to get public IPs
        instances_info = ec2.describe_instances(InstanceIds=instance_ids)
        # Get public IPs of started instances
        instance_ips = [
            instance.get('PublicIpAddress') 
            for reservation in instances_info['Reservations'] 
            for instance in reservation['Instances']
        ]

        print (f'Instance Ips: {instance_ips}')

    print(f"{action.capitalize()}d instances: {instance_ids}")
    print(response) if action == 'stop' else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="start /stop EC2 instances")
    parser.add_argument("action", choices=["start", "stop"], help="Action to perform")
    parser.add_argument("tag_key", help="Tag key to filter instances")
    parser.add_argument("tag_value", help="Tag value to filter instances")
    args = parser.parse_args()
    main(args.action, args.tag_key, args.tag_value)