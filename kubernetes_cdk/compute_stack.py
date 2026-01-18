import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from config import Config
from kubernetes_cdk.network_stack import NetworkStack


class ComputeStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, network_stack: NetworkStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create EC2 keypair
        self.key_pair = ec2.KeyPair(
            self, Config.KEY_PAIR_NAME
        )
        
        # Get the public subnet
        public_subnet = network_stack.vpc.public_subnets[0]
        
        # Create EC2 instance
        self.instance = ec2.Instance(
            self, "KubernetesInstance",
            vpc=network_stack.vpc,
            instance_type=ec2.InstanceType(Config.INSTANCE_TYPE),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2023
            ),
            key_pair=self.key_pair,
            vpc_subnets=ec2.SubnetSelection(subnets=[public_subnet]),
            security_group=network_stack.security_group,
            associate_public_ip_address=True
        )
        
        # Output the instance public IP
        cdk.CfnOutput(
            self, "InstancePublicIP",
            value=self.instance.instance_public_ip,
            description="Public IP of the Kubernetes instance"
        )