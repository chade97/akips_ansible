#!/usr/bin/env python

import os
import json
import requests
import sys
for a in os.environ:
    sys.stderr.write(' Var: ' + a + ' Value: ' + os.getenv(a) + "\n")

akips_server = os.environ['hostname']
password = os.environ['password']
group = os.environ['group']

url = 'https://{akips_server}/api-db?password={password};cmds=mget+*+*+ping4+PING.icmpState+value+/up/+any+group+{group}'

inventory = {'_meta': {'hostvars': {}}}

response = requests.get(url.format(akips_server=akips_server,
                                   password=password,
                                   group=group),
                        proxies={'http': None, 'https': None},
                        verify=os.path.dirname(os.path.realpath(__file__)) + "/cacert.cer")
lines = response.text.split('\n')
inventory[group] = {'hosts': []}

for line in lines:
    if line == '':
        continue
    host, _, _, _, data= line.split(' ')
    ip = data.split(',')[-1]
    inventory[group]['hosts'].append(host)
    inventory['_meta']['hostvars'][host] = {'ansible_host': ip}

print json.dumps(inventory)

