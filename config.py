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
    
    # Compute configurations for multiple instances
    COMPUTE_CONFIGS = {
        "master": {
            "instance_type": "t3.medium",
            "key_pair_name": "kubernetes-cdk-key",
            "count": 1,
            "scripts": ["scripts/user_data.txt", "scripts/master_init.sh"]
        },
        "worker": {
            "instance_type": "t3.small",
            "key_pair_name": "kubernetes-cdk-key",
            "count": 2,
            "scripts": ["scripts/user_data.txt", "scripts/worker_join.sh"]
        }
    }
    
    # Common scripts (executed on all instances)
    COMMON_SCRIPTS = [
        "scripts/common_setup.sh"
    ]
    USER_DATA_FILE = "scripts/user_data.txt"
