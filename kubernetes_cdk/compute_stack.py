import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2, aws_iam as iam
from constructs import Construct
from config import Config
from kubernetes_cdk.network_stack import NetworkStack


class ComputeStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, network_stack: NetworkStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create IAM role for SSM
        ssm_role = iam.Role(
            self, "SSMRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )
        
        self.instances = {}
        
        # Create instances based on compute configurations
        for config_name, config in Config.COMPUTE_CONFIGS.items():
            # Create EC2 keypair for this configuration
            key_pair = ec2.KeyPair(
                self, 
                f"{config['key_pair_name']}-{config_name}"
            )
            
            # Get the public subnet
            public_subnet = network_stack.vpc.public_subnets[0]
            
            # Create instances for this configuration
            for i in range(config['count']):
                instance_id = f"{config_name}-{i+1}"
                
                # Combine common scripts and instance-specific scripts
                combined_script = ""
                for script_path in Config.COMMON_SCRIPTS + config['scripts']:
                    with open(script_path, "r") as f:
                        combined_script += f.read() + "\n"
                
                instance = ec2.Instance(
                    self, f"Instance-{instance_id}",
                    vpc=network_stack.vpc,
                    instance_type=ec2.InstanceType(config['instance_type']),
                    machine_image=ec2.AmazonLinuxImage(
                        generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023
                    ),
                    key_pair=key_pair,
                    vpc_subnets=ec2.SubnetSelection(subnets=[public_subnet]),
                    security_group=network_stack.security_group,
                    associate_public_ip_address=True,
                    user_data=ec2.UserData.custom(combined_script),
                    role=ssm_role
                )
                
                self.instances[instance_id] = instance
                
                # Output the instance public IP
                cdk.CfnOutput(
                    self, f"Instance-{instance_id}-PublicIP",
                    value=instance.instance_public_ip,
                    description=f"Public IP of the {instance_id} instance"
                )