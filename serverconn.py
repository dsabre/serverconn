#!/usr/bin/env python

import json
import os.path
import sys
import fnmatch
import datetime
import subprocess
from subprocess import call

DIR = os.path.dirname(__file__)
SERVERS_DIR_NAME = 'servers'
BACKUP_DIR_NAME = 'backups'
SERVERS_DIRECTORY = DIR + "/servers"
CONFIGURATION_FILE_NAME = DIR + "/config.json"
BACKUP_COMMAND = 'b'
EDIT_COMMAND = 'e'

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


# return a list of all jsons found
def get_json_files():
    jsons = []
    for dirpath, dirnames, files in os.walk(SERVERS_DIRECTORY):
        for f in fnmatch.filter(files, '*.json'):
            jsons.append(dirpath + '/' + f)

    return sorted(jsons)


# obtain the servers list
def get_servers():
    i = 0
    servers = []

    for f in get_json_files():
        with open(f, 'r') as data:
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

        servers.append(data)

    return servers


# obtain a server from its id
def get_server(servers, id):
    for file in servers:
        for block in file:
            for server in block['servers']:
                if str(server['id']) == str(id):
                    return server


# connect to a server
def connect(servers, id):
    server = get_server(servers, id)

    try:
        if 'password' in server:
            call(["sshpass", "-p", server['password'], "ssh", "-o", "StrictHostKeyChecking=no", server['host']])
        else:
            call(["ssh", server['host']])
    except TypeError:
        print "Invalid server key"
        exit(3)


# print the servers table or list
def list_servers(servers, numColumns):
    rows = []

    for file in servers:
        for block in file:
            rows.append("---\n" + block['label'])
            row = []

            for server in block['servers']:
                serverLabel = server['alias'] if 'alias' in server else server['host']
                row.append(str(server['id']) + " - " + serverLabel)

                if len(row) == numColumns:
                    rows.append(("\t" if numColumns == 1 else "") + ("|".join(row)))
                    row = []

            rows.append("|".join(row))

    # add the configuration section
    rows.append("---\nConfiguration")
    rows.append("|".join([
        BACKUP_COMMAND + " - Backup the servers directory",
        EDIT_COMMAND + " - Edit the selected servers file"
    ]))

    print
    subprocess_cmd('echo "' + ("\n".join(rows)) + '" |column -t -s"|" |sed "s/---//g"')
    print


# execute a complex command
def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def backup_server_directory():
    # create the backup file name
    now = datetime.datetime.now()
    nowString = '' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
    backupFilename = SERVERS_DIR_NAME + '_' + nowString + '.tar.gz'

    # backup the servers
    subprocess.Popen(['tar', 'pczf', BACKUP_DIR_NAME + '/' + backupFilename, 'servers'], cwd=DIR)

    print
    print "Backup created: " + DIR + "/" + BACKUP_DIR_NAME + "/" + backupFilename
    print


def edit_servers_file():
    print
    print "Select the file to edit:"

    files = get_json_files()

    for k, file in enumerate(files):
        print '[' + str(k + 1) + '] ' + file

    fileId = 0
    try:
        fileId = int(raw_input('Enter the number of the file to edit: '))
    except ValueError:
        print "Invalid file number"
        exit(4)

    fileToEdit = ''
    try:
        fileToEdit = files[fileId - 1]
    except IndexError:
        print "Invalid file number"
        exit(4)

    call([get_configuration()['file_editor'], fileToEdit])


# main actions
configuration = get_configuration()
servers = get_servers()

# check if server files exists
if len(servers) == 0:
    print "No servers found"
    exit(1)

if len(sys.argv) == 2:
    if sys.argv[1] == BACKUP_COMMAND:
        backup_server_directory()
    elif sys.argv[1] == EDIT_COMMAND:
        edit_servers_file()
    else:
        # launch a clear if necessary
        if configuration['clear_before_connect']:
            call(['clear'])

        # try to connect to given server
        connect(servers, sys.argv[1])
else:
    # launch a clear if necessary
    if configuration['clear_before_list']:
        call(['clear'])

    # list servers
    list_servers(servers, configuration['num_table_columns'])
