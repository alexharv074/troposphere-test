from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2

from subprocess import check_output
import json
import os

class Jerakia:
    def lookup(self, key):
        os.environ["JERAKIA_CONFIG"] = "./jerakia.yaml"
        command = "bundle exec jerakia lookup %s --output json" % key
        json_string = check_output(command, shell=True)
        return json.loads(json_string)

class TropBase:
    jerakia = Jerakia()

    def write(self):
        self.template = Template()
        self.build()
        print(self.template.to_json())

class Ec2Instance(TropBase):
    def __init__(self):
        self.Mapping      = self.jerakia.lookup("Mapping")
        self.InstanceType = self.jerakia.lookup("InstanceType")

    def build(self):
        keyname_param = self.template.add_parameter(Parameter("KeyName",
            Description = "Name of an existing EC2 KeyPair to enable SSH access to the instance",
            Type        = "String",
        ))

        self.template.add_mapping("RegionMap", self.Mapping)

        ec2_instance = self.template.add_resource(ec2.Instance("Ec2Instance",
            ImageId        = FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
            InstanceType   = self.InstanceType,
            KeyName        = Ref(keyname_param),
            SecurityGroups = ["default"],
            UserData       = Base64("80"),
        ))

        self.template.add_output([Output("InstanceId",
            Description = "InstanceId of the newly created EC2 instance",
            Value       = Ref(ec2_instance),
        )])

Ec2Instance().write()
