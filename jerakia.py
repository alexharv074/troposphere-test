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

print Jerakia().lookup("baz")
