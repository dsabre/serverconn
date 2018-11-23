#!/usr/bin/env node

const index = require('./index');
const Table = require('cli-table');
require('colors');

module.exports.help = function(){
	let header = ['Description', 'Command example', 'Minimized command example'];
	for(let i = 0; i < header.length; i++){
		header[i] = header[i].bold.green;
	}
	
	const table = new Table({
		head : header,
		chars: { 'top': '' , 'top-mid': '' , 'top-left': '' , 'top-right': ''
			, 'bottom': '' , 'bottom-mid': '' , 'bottom-left': '' , 'bottom-right': ''
			, 'left': '' , 'left-mid': '' , 'mid': '' , 'mid-mid': ''
			, 'right': '' , 'right-mid': '' , 'middle': ' ' },
		style: { 'padding-left': 0, 'padding-right': 0 }
	});
	
	table.push([
		'To connect to a server:',
		'serverconn',
		'sc'
	]);
	table.push([
		'To connect to a server from id:',
		'serverconn --id=N',
		'sc --id=N'
	]);
	table.push([
		'To add a server:',
		'serverconn --add',
		'sc --add'
	]);
	table.push([
		'To remove a server:',
		'serverconn --remove',
		'sc --remove'
	]);
	table.push([
		'To remove a server from id:',
		'serverconn --remove --id=N',
		'sc --remove --id=N'
	]);
	table.push([
		'To list all servers:',
		'serverconn --list',
		'sc --list'
	]);
	table.push([
		'To list all servers of a category:',
		'serverconn --list --cat=Category',
		'sc --list --cat=Category'
	]);
	table.push([
		'To list a server with a specified id:',
		'serverconn --list --id=N',
		'sc --list --id=N'
	]);
	table.push([
		'To list a server with a specified id of a category:',
		'serverconn --list --cat=Category --id=N',
		'sc --list --cat=Category --id=N'
	]);
	table.push([
		'To manually edit the servers file:',
		'serverconn --edit',
		'sc --edit'
	]);
	
	console.log(('\nServerconn (' + index.VERSION + ') usage:').bold.yellow);
	console.log(table.toString());
	console.log('\n');
};
