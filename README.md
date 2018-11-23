# Serverconn
Permit to connect via ssh, in command line, to a server stored in a "database" json files.

## Installation
```bash
cd /your/prefered/directory
git clone https://github.com/raniel86/serverconn.git
cd serverconn
sudo npm i -g
```

## Usage
```
Description                                         Command example                         Minimized command example 
     
To connect to a server:                             serverconn                              sc                             
To connect to a server from id:                     serverconn --id=N                       sc --id=N                      
To add a server:                                    serverconn --add                        sc --add                       
To remove a server:                                 serverconn --remove                     sc --remove                    
To remove a server from id:                         serverconn --remove --id=N              sc --remove --id=N             
To list all servers:                                serverconn --list                       sc --list                      
To list all servers of a category:                  serverconn --list --cat=Category        sc --list --cat=Category       
To list a server with a specified id:               serverconn --list --id=N                sc --list --id=N               
To list a server with a specified id of a category: serverconn --list --cat=Category --id=N sc --list --cat=Category --id=N
To manually edit the servers file:                  serverconn --edit                       sc --edit
```
