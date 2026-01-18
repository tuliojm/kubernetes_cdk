import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from config import Config


class NetworkStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create VPC
        self.vpc = ec2.Vpc(
            self, "KubernetesVPC",
            ip_addresses=ec2.IpAddresses.cidr(Config.VPC_CIDR),
            max_azs=3,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="PublicSubnet",
                    cidr_mask=24,
                )
            ]
        )
        
        # Create security group
        self.security_group = ec2.SecurityGroup(
            self, "KubernetesSecurityGroup",
            vpc=self.vpc,
            description="Security group for Kubernetes cluster",
            allow_all_outbound=True
        )
        
        # Allow inbound SSH traffic from configured IP
        self.security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(Config.SSH_ALLOWED_IP),
            connection=ec2.Port.tcp(22),
            description="Allow SSH from configured IP"
        )