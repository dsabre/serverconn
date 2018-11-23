#!/usr/bin/env node

const index   = require('./index');
const prompts = require('prompts');
const fs      = require('file-system');
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
				removeServer(serversFlatten[argv.id - 1]);
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
				message : 'Select server to remove',
				choices : choices,
				suggest : suggestContain
			}).then(answer =>{
				for(let i = 0; i < serversFlatten.length; i++){
					if(answer.value !== serversFlatten[i].host){
						continue;
					}
					
					removeServer(serversFlatten[i]);
				}
			});
		}
	}
	else{
		console.error('No servers found'.red);
	}
});

function removeServer(server){
	prompts({
		type    : 'confirm',
		name    : 'value',
		message : 'Confirm remove ' + server.host + '?',
		initial : false
	}).then(answer =>{
		if(answer.value){
			index.getServersPath().then(serversPath =>{
				let serversContent = JSON.parse(fs.readFileSync(serversPath).toString());
				const categories   = Object.keys(serversContent);
				
				for(let i = 0; i < categories.length; i++){
					serversContent[categories[i]] = serversContent[categories[i]].filter(row =>{
						return Object.values(row).join('|') !== [server.host, server.username, server.password, server.port].join('|');
					});
				}
				
				fs.writeFile(serversPath, JSON.stringify(serversContent, null, 4));
				
				console.log('Server deleted corectly'.green);
			});
		}
	});
}