# About
This repository contains some usefull scripts for spacewalk maintenance.

## Configuration
You need at least a user with API access.
See spacewalk.yaml.example for valid configuration options.

## Scripts
### cleanup_swchannels.py
Removes any existing spacewalk software channels and repositories. Use this script if you want to remove any RPM related content.

# Limitation
Tested w/ spacewalk 2.5+ but might work with earlier versions.
