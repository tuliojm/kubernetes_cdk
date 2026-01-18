class Config:
    # Network configuration
    VPC_CIDR = "10.0.0.0/16"
    PUBLIC_SUBNET_CIDR = "10.0.1.0/24"
    SSH_ALLOWED_IP = "0.0.0.0/0"  # Change this to your IP for security
    
    # Compute configuration
    INSTANCE_TYPE = "t3.medium"
    KEY_PAIR_NAME = "kubernetes-cdk-key"