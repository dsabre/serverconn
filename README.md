# serverconn2
Permit to connect via ssh, in command line, to a server stored in a "database" json files.

## Installation
Simply create a json file in the _servers_ directory with this format:
```json
[
    {
        "label": "Section 1",
        "servers": [
            {"host": "username@myserver.com", "id": "fixed_id"}
        ]
    },
    {
        "label": "Section 2",
        "servers": [
            {"host": "username@myserver2.com"},
            {"host": "username@255.255.255.255", "alias": "Super server!"},
            {"host": "username@myserver3.com", "password": "mystrongpassword"}
        ]
    }
]
```
Every server is defined by a json object, the most complex object is this:
```json
{"host": "username@255.255.255.255", "id": "fixed_id", "alias": "Super server!", "password": "mystrongpassword"}
```
- **host** (required): is the server where you want to connect in, the format is "username@server" or simply "server" if you want to use your local username,
- **id** (optional): if you want that the program use the same id for the server, you can fix it here,
- **alias** (optional): if defined it will be used to identify the server in the server list,
- **password** (optional): here you can specify the password to use for the connection.

## Configuration
In the _config.json_ file you can modify the behavior of the program:
- **num_table_columns**: identify the number of table columns for the server list,
- **clear_before_list**: if true this will clear the console before show the servers list,
- **clear_before_connect**: if true this will clear the console before connect to a server.

## Usage
Enter, via command line, in the directory of serverconn2 and type:

To list all servers:
```commandline
./serverconn.py
```

To connect to a server:
```commandline
./serverconn.py [SERVER_ID]
```