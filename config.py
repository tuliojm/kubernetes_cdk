class Config:
    # General configuration
    GENERAL_TAGS = {
        "project_name": "kubernetes-cdk",
        "environment": "dev",
    }

    # Network configuration
    VPC_CIDR = "10.0.0.0/16"
    PUBLIC_SUBNET_CIDR = "10.0.1.0/24"
    SSH_ALLOWED_IP = "1.2.3.4/32"  # Change this to your IP for security
    
    # Compute configuration
    INSTANCE_TYPE = "t3.medium"
    KEY_PAIR_NAME = "kubernetes-cdk-key"
    USER_DATA_FILE = "scripts/user_data.txt"
