import boto3
from utils import get_keys_by_tag, get_private_key_from_ssm
import argparse
import os

def main(tag_key, tag_value):
    key_ids = get_keys_by_tag(tag_key, tag_value)
    home = os.getenv('HOME')

    if not key_ids:
        print("No keys found.")
        return
    for key_id in key_ids:
        private_keys = get_private_key_from_ssm([key_id])
        for private_key in private_keys:
            with open(f'{home}/.ssh/{key_id}.pem', 'w') as key_file:
                key_file.write(private_key)
            print(f'Private key for key ID {key_id} written to {home}/.ssh/{key_id}.pem')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="start /stop EC2 instances")
    parser.add_argument("tag_key", help="Tag key to filter instances")
    parser.add_argument("tag_value", help="Tag value to filter instances")
    args = parser.parse_args()
    main(args.tag_key, args.tag_value)    