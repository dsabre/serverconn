#!/usr/bin/env node

const index = require('./index');
const Table = require('cli-table');
require('colors');

module.exports.listServers = function(){
	const argv = require('minimist')(process.argv.slice(2));
	
	let header = ['ID', 'Category', 'Host', 'Username', 'Password', 'Port'];
	for(let i = 0; i < header.length; i++){
		header[i] = header[i].bold.green;
	}
	
	const table = new Table({
		head : header
	});
	
	index.getServersFlatten().then(serversFlatten =>{
		for(let i = 0; i < serversFlatten.length; i++){
			if(argv.cat && argv.cat !== serversFlatten[i].category){
				continue;
			}
			
			if(argv.id && argv.id !== serversFlatten[i].id){
				continue;
			}
			
			table.push([
				serversFlatten[i].id,
				serversFlatten[i].category,
				serversFlatten[i].host,
				serversFlatten[i].username,
				serversFlatten[i].password,
				serversFlatten[i].port
			]);
		}
		
		console.log('SERVERS FOUND:'.bold.yellow);
		console.log(table.toString());
	});
};
