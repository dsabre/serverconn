#!/usr/bin/env node

const index   = require('./index');
const prompts = require('prompts');
const ssh     = require('ssh2-client');
require('colors');

const argv = require('minimist')(process.argv.slice(2));

index.getServersFlatten().then(serversFlatten =>{
	if(serversFlatten.length > 0){
		let choices = [];
		for(let i = 0; i < serversFlatten.length; i++){
			choices.push({
				title : serversFlatten[i].username + '@' + serversFlatten[i].host,
				value : serversFlatten[i].host
			});
		}
		
		if(argv.id){
			if(serversFlatten[argv.id - 1]){
				connect(serversFlatten[argv.id - 1]);
			}
			else{
				console.error('Invalid server id'.red);
			}
		}
		else{
			const suggestContain = (input, choices) =>{
				return Promise.resolve(choices.filter(i =>{
					return i.title.indexOf(input) > -1;
				}));
			};
			
			prompts({
				type    : 'autocomplete',
				name    : 'value',
				message : 'Select server to connect',
				choices : choices,
				suggest : suggestContain
			}).then(answer =>{
				for(let i = 0; i < serversFlatten.length; i++){
					if(answer.value !== serversFlatten[i].host){
						continue;
					}
					
					connect(serversFlatten[i]);
				}
			});
		}
	}
	else{
		console.error('No servers found'.red);
	}
});

function connect(server){
	//let command = 'ssh ' + server.username + '@' + server.host;
	//if(server.password){
	//	command = 'sshpass -p "' + server.password + '" ssh -o StrictHostKeyChecking=no ' + server.username + '@' + server.host;
	//}
	
	const HOST    = server.username + '@' + server.host;
	const OPTIONS = {
		password : server.password
	};
	
	ssh
	.shell(HOST, OPTIONS)
	.then(() => console.log(('\nClosed connection on ' + HOST + '\n').yellow))
	.catch(err => console.error('\n' + err.message.red + '\n'));
}