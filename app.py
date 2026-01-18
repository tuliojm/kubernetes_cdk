#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from kubernetes_cdk.kubernetes_cdk_stack import KubernetesCdkStack
from kubernetes_cdk.network_stack import NetworkStack
from kubernetes_cdk.compute_stack import ComputeStack



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

# KubernetesCdkStack(app, "KubernetesCdkStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.

#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.

#     env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */

#     #env=cdk.Environment(account='123456789012', region='us-east-1'),

#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#     )

app.synth()
