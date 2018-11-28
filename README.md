# Jerakia example

This repo contains an example of the simplest Jerakia set up in a bundle-based installation.

# Usage

Clone this repo.

```text
bundle install
JERAKIA_CONFIG=./jerakia.yaml bundle exec jerakia lookup --log-level=debug foo
bar
```

# Known issues

This led to the installation of Jerakia 2.5.0 which seems to have a bug in the option handling logic. I worked around this by reading the code and setting the `$JERAKIA_CONFIG` environment variable rather than passing `--config=./jerakia.yaml`.
