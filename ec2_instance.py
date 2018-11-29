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

class Ec2Instance:
    def __init__(self):
        jerakia = Jerakia()
        self.Mapping      = jerakia.lookup("Mapping")
        self.InstanceType = jerakia.lookup("InstanceType")

    def write(self):
        template = Template()

        keyname_param = template.add_parameter(Parameter("KeyName",
            Description = "Name of an existing EC2 KeyPair to enable SSH access to the instance",
            Type        = "String",
        ))

        template.add_mapping("RegionMap", self.Mapping)

        ec2_instance = template.add_resource(ec2.Instance("Ec2Instance",
            ImageId        = FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
            InstanceType   = self.InstanceType,
            KeyName        = Ref(keyname_param),
            SecurityGroups = ["default"],
            UserData       = Base64("80"),
        ))

        template.add_output([Output("InstanceId",
            Description = "InstanceId of the newly created EC2 instance",
            Value       = Ref(ec2_instance),
        )])

        print(template.to_json())

Ec2Instance().write()
