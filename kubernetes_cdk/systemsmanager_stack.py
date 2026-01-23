import os
from aws_cdk import (
    Stack,
    aws_ssm as ssm,
)
from constructs import Construct
from config import Config


class SystemsManagerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create separate SSM documents for each compute configuration
        for config_name, config in Config.COMPUTE_CONFIGS.items():
            # Combine common scripts and instance-specific scripts
            scripts = Config.COMMON_SCRIPTS + config['scripts']
            combined_script = ""
            for script_path in scripts:
                full_path = os.path.join(os.path.dirname(__file__), "..", script_path)
                with open(full_path, 'r') as f:
                    combined_script += f.read() + "\n"

            # SSM Document for this configuration
            config_document = ssm.CfnDocument(
                self, f"ConfigurationDocument-{config_name}",
                document_type="Command",
                document_format="YAML",
                content={
                    "schemaVersion": "2.2",
                    "description": f"Configure {config_name} instances",
                    "mainSteps": [
                        {
                            "action": "aws:runShellScript",
                            "name": "configureInstance",
                            "inputs": {
                                "runCommand": [combined_script]
                            }
                        }
                    ]
                }
            )

            # State Manager Association for this configuration
            ssm.CfnAssociation(
                self, f"ConfigurationAssociation-{config_name}",
                name=config_document.ref,
                targets=[
                    {
                        "key": "tag:InstanceType",
                        "values": [config_name]
                    }
                ],
                schedule_expression="rate(30 minutes)"
            )