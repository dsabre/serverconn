#!/usr/bin/env python

import json
import os.path
import sys
import subprocess
from subprocess import call

DIR = os.path.dirname(__file__)
SERVERS_FILE_NAME = DIR + "/servers.json"
CONFIGURATION_FILE_NAME = DIR + "/config.json"

# check if server file exists
if not os.path.isfile(SERVERS_FILE_NAME):
    print SERVERS_FILE_NAME + " not found"
    exit(1)

# check if config file exists
if not os.path.isfile(CONFIGURATION_FILE_NAME):
    print CONFIGURATION_FILE_NAME + " not found"
    exit(1)


# obtain the main configuration
def get_configuration():
    with open(CONFIGURATION_FILE_NAME, 'r') as config:
        try:
            return json.load(config)
        except ValueError:
            print "Invalid json format"
            exit(2)


# obtain the servers list
def get_servers():
    i = 0

    with open(SERVERS_FILE_NAME, 'r') as data:
        try:
            data = json.load(data)
        except ValueError:
            print "Invalid json format"
            exit(2)

    for k, block in enumerate(data):
        for l, server in enumerate(block['servers']):
            i = i + 1
            if 'id' not in server:
                data[k]['servers'][l]['id'] = i

    return data


# obtain a server from its id
def get_server(id):
    for block in get_servers():
        for server in block['servers']:
            if str(server['id']) == str(id):
                return server


# connect to a server
def connect(id):
    server = get_server(id)
    try:
        if 'password' in server:
            call(["sshpass", "-p", server['password'], "ssh", "-o", "StrictHostKeyChecking=no", server['host']])
        else:
            call(["ssh", server['host']])
    except TypeError:
        print "Invalid server key"
        exit(3)


# print the servers table or list
def list_servers(numColumns):
    rows = []

    for block in get_servers():
        rows.append("---\n" + block['label'])
        row = []

        for server in block['servers']:
            row.append(str(server['id']) + " - " + server['host'])

            if len(row) == numColumns:
                rows.append(("\t" if numColumns == 1 else "") + ("|".join(row)))
                row = []

        rows.append("|".join(row))

    print
    subprocess_cmd('echo "' + ("\n".join(rows)) + '" |column -t -s"|" |sed "s/---//g"')
    print


# execute a complex command
def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


# main actions
configuration = get_configuration()

if len(sys.argv) == 2:
    # launch a clear if necessary
    if configuration['clear_before_connect']:
        call(['clear'])

    # try to connect to given server
    connect(sys.argv[1])
else:
    # launch a clear if necessary
    if configuration['clear_before_list']:
        call(['clear'])

    # list servers
    list_servers(configuration['num_table_columns'])
