# Troposphere + Jerakia example

This repo contains a proof of concept [Troposphere](https://github.com/cloudtools/troposphere) with [Jerakia](http://jerakia.io) as an external Hiera-like data store.

# Usage

Clone this repo. Cd into it.

## Test Jerakia

```text
$ bundle install
$ JERAKIA_CONFIG=./jerakia.yaml bundle exec jerakia lookup foo
bar
```

## Test Troposphere

Set up a virtualenv:

```text
virtualenv ./virtualenv
source ./virtualenv/bin/activate
pip install -r requirements.txt
```

Run the ec2_instance.py script:

```text
python ec2_instance.py > ec2.json
```

This writes out a Cloudformation JSON file.

## Create stack

```text
aws cloudformation create-stack --template-body file://ec2.json
```

# python-jerakia

At the time of writing, a python client [python-jerakia](https://github.com/jerakia/python-jerakia) exists, but I found there was no PIP package available and it seemed to require a Jerakia Server to be running, whereas I wanted this all to run in a Python Virtualenv/Bundle. For now, I've just used subprocess in Python to call Bundler.

# Known issues

At the time of writing, the latest Jerakia available at Rubygems.org was version 2.5.0 which seems to have a bug in the option handling logic. I worked around this by reading the code and setting the `$JERAKIA_CONFIG` environment variable rather than passing `--config=./jerakia.yaml`.
