#!/usr/bin/python
#
# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('path', default='/var/lib/os-collect-config/local-data')
parser.add_argument('--deployments-key', default='deployments')

args = parser.parse_args()

for fname in os.listdir(args.path):
    f = os.path.join(args.path, fname)
    with open(f) as infile:
        x = json.loads(infile.read())
        dp = args.deployments_key
        final_list = []
        if dp in x:
            if isinstance(x[dp], list):
                for d in x[dp]:
                    name = d['name']
                    if d.get('group', 'Heat::Ungrouped') in (
                        'os-apply-config',
                        'Heat::Ungrouped'
                    ):
                        final_list.append((name, d['config']))
    for oname, oconfig in final_list:
        with open('%s%s' % (f, oname), 'w') as outfile:
            outfile.write(json.dumps(oconfig))
