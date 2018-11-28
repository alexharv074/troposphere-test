# Jerakia example

This repo contains an example of the simplest [Jerakia](http://jerakia.io) set up in a bundle-based installation.

# Usage

Clone this repo.

```text
$ bundle install
$ JERAKIA_CONFIG=./jerakia.yaml bundle exec jerakia lookup foo
bar
```

# Known issues

At the time of writing, the latest Jerakia available at Rubygems.org was version 2.5.0 which seems to have a bug in the option handling logic. I worked around this by reading the code and setting the `$JERAKIA_CONFIG` environment variable rather than passing `--config=./jerakia.yaml`.
