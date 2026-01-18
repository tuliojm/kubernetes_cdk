import aws_cdk as core
import aws_cdk.assertions as assertions

from kubernetes_cdk.kubernetes_cdk_stack import KubernetesCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in kubernetes_cdk/kubernetes_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = KubernetesCdkStack(app, "kubernetes-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
