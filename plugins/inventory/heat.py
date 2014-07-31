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


def parse_args():
    parser = argparse.ArgumentParser(description='Heat inventory module')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true',
                       help='List active servers')
    group.add_argument('--host', help='List details about the specific host')
    return parser.parse_args()

def _list(stack_name):
    hostvars = {}
    groups = {}
    # XXX: need to config access details
    client = heat_client.Client()
    for res in client.stacks.get(stack_name).resources:
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
            hostvars[addr] = {'heat_metadata': res.metadata} 
    inventory = {'_meta': {'hostvars': hostvars}}
    inventory.update(groups)
    print(json.dumps(inventory, indent=2))

def main():
    args = parse_args()
    if args.list:
        _list(os.environ['OS_STACK_NAME'])
    elif args.host:
        _host(args.host)
    sys.exit(0)

if __name__ == '__main__':
    main()
