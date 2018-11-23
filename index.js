#!/usr/bin/env node

const fs = require('file-system');
require('colors');

const argv = require('minimist')(process.argv.slice(2));

module.exports.SERVER_FILE = 'servers.json';
module.exports.CONFIG_FILE = 'config.json';
module.exports.VERSION = 'v3.0.0';

module.exports.getUsername = function(){
	return require('username')();
};

module.exports.getConfigDir = function(){
	return module.exports.getUsername().then(username =>{
		return '/home/' + username + '/.serverconn';
	});
};

module.exports.getServersPath = function(){
	return module.exports.getConfigDir().then(dir =>{
		return dir + '/' + module.exports.SERVER_FILE;
	});
};

module.exports.setConfig = function(key, value){
	return module.exports.getConfig().then(config => {
		return module.exports.getConfigDir().then(dir => {
			config[key] = value;
			
			fs.writeFile(dir + '/' + module.exports.CONFIG_FILE, JSON.stringify(config, null, 4));
			
			return config;
		});
	});
};

module.exports.getConfig = function(){
	return module.exports.getConfigDir().then(dir => {
		let config = {};
		try{
			config = JSON.parse(fs.readFileSync(dir + '/' + module.exports.CONFIG_FILE));
		}
		catch(e){
			config = {};
		}
		
		return config;
	});
};

module.exports.getServersFlatten = function(){
	let key = 1;
	return module.exports.getServersPath().then(serversPath =>{
		try{
			const serversContent = JSON.parse(fs.readFileSync(serversPath).toString());
			const categories     = Object.keys(serversContent);
			let serversFlatten   = [];
			
			for(let i = 0; i < categories.length; i++){
				const servers = serversContent[categories[i]];
				
				for(let k = 0; k < servers.length; k++){
					servers[k].id       = key++;
					servers[k].category = categories[i];
					
					serversFlatten.push(servers[k]);
				}
			}
			
			return serversFlatten;
		}
		catch(e){
			return [];
		}
	});
};

if(argv.add){
	require('./add').addServer();
	return;
}
else if(argv.list){
	require('./list').listServers();
	return;
}
else if(argv.remove){
	require('./remove');
	return;
}
else if(argv.version){
	console.log('Serverconn version: ' + (module.exports.VERSION.bold));
	return;
}
else if(argv.help){
	require('./help').help();
	return;
}
else if(argv.edit){
	require('./edit');
	return;
}

require('./connect');
