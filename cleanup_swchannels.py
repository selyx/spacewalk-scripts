#!/usr/bin/env python
# vim: ts=8 et sw=4 sts=4
import xmlrpclib
import yaml
import glob
import os

home = os.getenv("HOME")
with open(home + '/.spacewalk.yaml', 'r') as config:
    cfg = yaml.safe_load(config)
    SPACEWALK_URL = cfg['spacewalk_api']
    SPACEWALK_LOGIN = cfg['spacewalk_user']
    SPACEWALK_PASSWORD = cfg['spacewalk_password']
    channel_blacklist = cfg['channel_blacklist'] if 'channel_blacklist' in cfg.keys() else []
    repo_blacklist = cfg['repo_blacklist'] if 'repo_blacklist' in cfg.keys() else []


def main():
    client = xmlrpclib.Server(SPACEWALK_URL, verbose=0)
    key = client.auth.login(SPACEWALK_LOGIN, SPACEWALK_PASSWORD)

    channels = client.channel.listSoftwareChannels(key)
    parent_channels = [s['label'] for s in channels if s['parent_label'] == '' ]
    child_channels = [s['label'] for s in channels if s['parent_label'] != '' ]
    
    for channel in child_channels + parent_channels:
        if channel in channel_blacklist:
            print('skipping blacklisted channel ' + channel)
            continue
        print('removing channel ' + channel)
        client.channel.software.delete(key, channel)
        

    repos = client.channel.software.listUserRepos(key)
    for r in repos:
        repo = r['label']
        if repo in repo_blacklist:
            print('skipping blacklisted repo ' + repo)
            continue

        print('removing repositories ' + repo)
        client.channel.software.removeRepo(key, repo)

    client.auth.logout(key)
    print('Done!')


if __name__ == '__main__':
    main()
