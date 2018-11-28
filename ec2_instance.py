from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2

from subprocess import check_output
import json
import os

class Jerakia:
    def __init__(self):
        pass

    def lookup(self, key):
        os.environ["JERAKIA_CONFIG"] = "./jerakia.yaml"
        command = "bundle exec jerakia lookup %s --output json" % key
        json_string = check_output(command, shell=True)
        return json.loads(json_string)

class Troposphere:
    def __init__(self):
        pass

    def write(self):
        template = Template()
        jerakia  = Jerakia()

        keyname_param = template.add_parameter(Parameter(
            "KeyName",
            Description="Name of an existing EC2 KeyPair to enable SSH "
                        "access to the instance",
            Type="String",
        ))

        template.add_mapping('RegionMap', jerakia.lookup("Mapping"))

        ec2_instance = template.add_resource(ec2.Instance(
            "Ec2Instance",
            ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
            InstanceType=jerakia.lookup("InstanceType"),
            KeyName=Ref(keyname_param),
            SecurityGroups=["default"],
            UserData=Base64("80")
        ))

        template.add_output([
            Output(
                "InstanceId",
                Description="InstanceId of the newly created EC2 instance",
                Value=Ref(ec2_instance),
            ),
        ])

        print(template.to_json())

t = Troposphere()
t.write()
