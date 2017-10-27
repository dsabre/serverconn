#!/usr/bin/env python

import json
import os.path
from os import listdir
from os.path import isfile, join
import sys
import fnmatch
import datetime
import subprocess
from subprocess import call

DIR = os.path.dirname(__file__)
SERVERS_DIR_NAME = 'servers'
BACKUP_DIR_NAME = 'backups'
SERVERS_DIRECTORY = DIR + "/" + SERVERS_DIR_NAME
CONFIGURATION_FILE_NAME = DIR + "/config.json"
BACKUP_DATE_FORMAT = '%Y%m%d%H%M%S'
BACKUP_EXTENSION = '.tar.gz'

# commands definitions
BACKUP_COMMAND = 'b'
RESTORE_BACKUP_COMMAND = 'r'
EDIT_COMMAND = 'e'
EDIT_CONF_COMMAND = 'c'
ADD_SERVER_COMMAND = 'a'

# check if config file exists
if not os.path.isfile(CONFIGURATION_FILE_NAME):
    print CONFIGURATION_FILE_NAME + " not found"
    exit(1)

configuration = {}
with open(CONFIGURATION_FILE_NAME, 'r') as config:
    try:
        configuration = json.load(config)
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


# get the json data of a file
def get_json_data_from_file(file):
    with open(file, 'r') as data:
        try:
            return json.load(data)
        except ValueError:
            print "Invalid json format"
            exit(2)


# obtain the servers list
def get_servers():
    i = 0
    servers = []

    for f in get_json_files():
        data = get_json_data_from_file(f)

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
        print "Invalid command key"
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

    commands = {
        BACKUP_COMMAND: "Backup the servers directory",
        RESTORE_BACKUP_COMMAND: "Restore a previous created backup",
        EDIT_COMMAND: "Edit the selected servers file",
        EDIT_CONF_COMMAND: "Edit the configuration file",
        ADD_SERVER_COMMAND: "Add server to file"
    }
    row = []
    for command, label in commands.items():
        row.append(command + ' - ' + label)

        if len(row) == numColumns:
            rows.append(("\t" if numColumns == 1 else "") + ("|".join(row)))
            row = []
    rows.append("|".join(row))

    if not configuration['clear_before_list']:
        print

    subprocess_cmd('echo "' + ("\n".join(rows)) + '" |column -t -s"|" |sed "s/---//g"')
    print


# execute a complex command
def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


# execute a backup of the entire servers directory
def backup_server_directory():
    # create the backup file name
    now = datetime.datetime.now()
    backupFilename = SERVERS_DIR_NAME + '_' + (now.strftime(BACKUP_DATE_FORMAT)) + BACKUP_EXTENSION

    # backup the servers
    subprocess.Popen(['tar', 'pczf', BACKUP_DIR_NAME + '/' + backupFilename, SERVERS_DIR_NAME], cwd=DIR)

    print
    print "Backup created: " + DIR + "/" + BACKUP_DIR_NAME + "/" + backupFilename
    print


# restore a backup file
def restore_backup_server_directory():
    backupPath = DIR + "/" + BACKUP_DIR_NAME
    files = [f for f in listdir(backupPath) if isfile(join(backupPath, f)) and fnmatch.fnmatch(f, '*' + BACKUP_EXTENSION)]

    print
    print "Enter the number of the backup to restore: "
    print
    for k, file in enumerate(files):
        fileCreationDate = file.replace(BACKUP_EXTENSION, '').split('_')[1]
        fileCreationDate = datetime.datetime.strptime(fileCreationDate, BACKUP_DATE_FORMAT)
        fileCreationDate = fileCreationDate.strftime('%Y-%m-%d %H:%M:%S')

        print '[' + str(k + 1) + '] ' + file + ' (created at: ' + fileCreationDate + ')'
    print

    backupId = int(raw_input('Backup id: ')) - 1

    subprocess.Popen(['rm', '-rf', SERVERS_DIR_NAME], cwd=DIR)
    subprocess.Popen(['tar', 'xf', BACKUP_DIR_NAME + '/' + files[backupId]], cwd=DIR)


# open the configuration file for edit
def edit_configuration_file():
    call([configuration['file_editor'], CONFIGURATION_FILE_NAME])


# open a servers file for edit
def edit_servers_file():
    print
    print "Select the file to edit:"

    files = get_json_files()

    for k, file in enumerate(files):
        print '[' + str(k + 1) + '] ' + file

    print

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

    call([configuration['file_editor'], fileToEdit])


def add_server(args):
    files = get_json_files()

    # get the id of file where add the server
    fileId = 0
    try:
        # try to get from command params
        fileId = int(args[2])
    except IndexError:
        try:
            print
            print 'Enter the number of the file where you want to add the server: '

            for k, file in enumerate(files):
                print '[' + str(k + 1) + '] ' + file

            fileId = int(raw_input('File id: '))
        except ValueError:
            print "Invalid file number"
            exit(4)

    # get the file to edit
    fileToEdit = ''
    try:
        fileToEdit = files[fileId - 1]
    except IndexError:
        print "Invalid file number"
        exit(4)

    # get the id of the block where add the server
    blockId = 0
    data = get_json_data_from_file(fileToEdit)
    try:
        # try to get from command params
        blockId = int(args[3])
    except IndexError:
        if len(data) > 1:
            print
            print 'Enter the number of the block where you want to add the server:'

            for k, block in enumerate(data):
                print '[' + str(k + 1) + '] ' + block['label']

            blockId = int(raw_input('Block id: '))
        else:
            blockId = 0

    # create the server object
    newServer = {}

    # get server host
    host = None
    hostArgIndex = 4
    try:
        # try to get from command params
        host = args[hostArgIndex]
    except IndexError:
        while(not host):
            host = raw_input('Host (required): ')
    newServer['host'] = host

    # get the optional parameters
    optionalParameters = {
        "id": 'Fixed id: ',
        "alias": 'Alias: ',
        "password": 'Password: ',
    }
    i = 1
    for k, question in optionalParameters.items():
        try:
            # try to get from command params
            value = args[hostArgIndex + i]
        except IndexError:
            value = raw_input(question)

        if value:
            newServer[k] = value

        i = i + 1

    # add server to others
    data[blockId - 1]['servers'].append(newServer)

    # transform data in a json
    data = json.dumps(data, False, True, True, True, None, 4, None, 'utf-8', None, True)

    # write data on file
    file = open(fileToEdit, "w")
    file.write(data)
    file.close()

    print
    print "Server added correctly"
    print


# main actions
servers = get_servers()


# execute the user selected operation
def execute_operation(operation):
    if operation == BACKUP_COMMAND:
        backup_server_directory()
    elif operation == RESTORE_BACKUP_COMMAND:
        restore_backup_server_directory()
    elif operation == EDIT_COMMAND:
        edit_servers_file()
    elif operation == EDIT_CONF_COMMAND:
        edit_configuration_file()
    elif operation == ADD_SERVER_COMMAND:
        add_server(sys.argv)
    else:
        try:
            operation = int(operation)
        except ValueError:
            print
            print "Invalid command key"
            print
            exit(3)

        # launch a clear if necessary
        if configuration['clear_before_connect']:
            call(['clear'])

        # try to connect to given server
        connect(servers, operation)


if len(sys.argv) > 1:
    execute_operation(sys.argv[1])
else:
    # launch a clear if necessary
    if configuration['clear_before_list']:
        call(['clear'])

    # check if server files exists
    if len(servers) == 0:
        print
        print "No servers found"
        print

    # list servers
    list_servers(servers, configuration['num_table_columns'])

    if configuration['fluent_operation']:
        execute_operation(raw_input('Choice: '))
