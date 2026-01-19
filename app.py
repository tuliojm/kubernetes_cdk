#!/usr/bin/env python3
import os

import aws_cdk as cdk

from kubernetes_cdk.network_stack import NetworkStack
from kubernetes_cdk.compute_stack import ComputeStack

from config import Config

app = cdk.App()

# Create Network stack
network_stack = NetworkStack(
    app, "NetworkStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

# Create Compute stack with dependency on Network stack
compute_stack = ComputeStack(
    app, "ComputeStack",
    network_stack=network_stack,
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

if isinstance(Config.GENERAL_TAGS, dict):
    for key, value in Config.GENERAL_TAGS.items():
        cdk.Tags.of(app).add(key, value)

app.synth()
