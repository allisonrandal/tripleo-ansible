#!/usr/bin/env python
DOCUMENTATION = '''
---
inventory: heat
short_description: Heat external inventory script
description:
    - Generates inventory that Ansible can understand by making API requests to
      Heat and Nova API
options:
    stack:
        description:
        - Identifier (name or ID) for heat stack to interrogate.
requirements: [ "heatclient" ]
'''

import argparse
import os
import sys

from oslo.config import cfg

opts = [
        cfg.StrOpt('host', help='List details about the specific host'),
        cfg.BoolOpt('list', help='List active hosts'),
        cfg.MultiStrOpt('stack', help='Stack IDs or Names to inspect',
            positional=True),
        cfg.StrOpt('os-username'),
        cfg.StrOpt('os-password'),
        cfg.StrOpt('os-auth-url'),
        ]

try:
    from heatclient.v1 import client as heat_client
except ImportError:
    print('heatclient is required')
    sys.exit(1)
try:
    from novaclient.v1_1 import client as nova_client
except ImportError:
    print('novaclient is required')
    sys.exit(1)


def _parse_config():
    configs = cfg.ConfigOpts()
    configs.register_cli_opts(opts)
    configs(prog='heat-ansible-inventory')
    return configs

class HeatInventory(object):
    def __init__(self, configs):
        self.configs = configs
        self._ksclient = None
        self._hclient = None

    def _list(self)
        hostvars = {}
        groups = {}
        # XXX: need to config access details
        for stack in configs.stack:
            stack_obj = self.hclient.stacks.get(stack)
            stack_id = stack_obj.id
            for res in self.hclient.resources.list(stack_id):
                if res.type == 'OS::Nova::Server':
                    server = nova_client.show(res.instance_id)
                    name = server.name
                    private = [ x['addr'] for x in getattr(server,
                                                           'addresses').itervalues().next()
                               if x['OS-EXT-IPS:type'] == 'fixed']
                    public  = [ x['addr'] for x in getattr(server,
                                                           'addresses').itervalues().next()
                               if x['OS-EXT-IPS:type'] == 'floating']

                    addr = server.accessIPv4 or public or private
                    groups[res.instance_id] = [addr]
                    groups[server.name] = [addr]
                    # TODO: group by image name
                    hostvars[addr] = {'heat_metadata':
                        self.hclient.resources.metadata(stack_id, res)}
        inventory = {'_meta': {'hostvars': hostvars}}
        inventory.update(groups)
        print(json.dumps(inventory, indent=2))

    @property
    def ksclient(self):
        if self._ksclient is None:
            self._ksclient = keystone_client.Client(
                    auth_url=self.configs.auth_url,
                    username=self.configs.username,
                    password=self.configs.password)
        return self._ksclient

    @property
    def hclient(self):
        if self._hclient is None:
            ksclient = self.ksclient
            endpoint = ksclient.service_catalog.url_for(
                    service_type='orchestration', endpoint_type='publicURL')
            self._hclient = heat_client.Client(
                    endpoint=endpoint,
                    auth_ref=ksclient.get_auth_ref())
        return self._hclient


def main():
    configs = _parse_args()
    hi = HeatInventory(configs)
    if args.list:
        hi.list()
    elif args.host:
        hi.host()
    sys.exit(0)

if __name__ == '__main__':
    main()
