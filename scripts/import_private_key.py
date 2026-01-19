import boto3
from utils import get_instances

def main():
    # Get instance IDs with specific tag
    # get_instances wasn't created for this so using "stop" action to get running instances
    # TODO: Refactor get_instances to be more flexible  
    # instace_ids = get_instances('stop', 'project_name', 'kubernetes-cdk')
    # if len(instace_ids) == 0:
    #     print("No instances found.")
    #     return
    # key_id = instace_ids[0].strip('i-')
    key_id = '0d7fbedcb8599f0a7'
    print(f"Instance ID: {key_id}")
    # Get key from System Manager Parameter Store
    ssm = boto3.client('ssm')
    parameter_name = f'/ec2/keypair/key-{key_id}'
    response = ssm.get_parameter(
        Name=parameter_name,
        WithDecryption=True # Ensure the parameter is decrypted if it's a SecureString 
    )
    private_key = response['Parameter']['Value']
    print(private_key)

if __name__ == "__main__":
    main()
    