#!/usr/bin/env node

const index        = require('./index');
// const openInEditor = require('open-in-editor');
// const prompts      = require('prompts');
// require('colors');

// const { exec } = require('child_process');
const openEditor = require('open-editor');

index.getServersPath().then(path =>{
	openEditor([path]);
});
// index.getServersPath().then(path =>{
// 	exec('vim ' + path, (err, stdout, stderr) => {
// 		if (err) {
// 			// node couldn't execute the command
// 			return;
// 		}
//
// 		// the *entire* stdout and stderr (buffered)
// 		console.log((`stdout: ${stdout}`).cyan);
// 		console.error((`stderr: ${stderr}`).red);
// 	});
// });

// index.getServersPath().then(path =>{
// 	index.getConfig().then(config => {
// 		const choices = [
// 			{
// 				title : 'Sublime',
// 				value : 'sublime'
// 			},
// 			{
// 				title : 'Atom',
// 				value : 'atom'
// 			},
// 			{
// 				title : 'Webstorm',
// 				value : 'webstorm'
// 			},
// 			{
// 				title : 'Phpstorm',
// 				value : 'phpstorm'
// 			},
// 			{
// 				title : 'Vim',
// 				value : 'vim'
// 			}
// 		];
//
// 		let initial = 0;
// 		if(config.defaultEditor){
// 			for(initial; initial < choices.length; initial++){
// 				if(choices[initial].value === 'atom'){
// 					break;
// 				}
// 			}
// 		}
//
// 		prompts({
// 			type    : 'select',
// 			name    : 'value',
// 			message : 'Select editor',
// 			choices : choices,
// 			initial : initial
// 		}).then(answers =>{
// 			if(answers.value){
// 				index.setConfig('defaultEditor', answers.value).then(newConfig => {
// 					const editor = openInEditor.configure({
// 						editor : answers.value
// 					}, function(err){
// 						console.error(('Something went wrong: ' + err).red);
// 						console.log(('Try to open manually: ' + path).yellow);
// 					});
//
// 					editor.open(path)
// 					.then(function(){
// 						console.log('Opening file with ' + answers.value + '...');
// 					}, function(err){
// 						console.error(('Something went wrong: ' + err).red);
// 						console.log(('Try to open manually: ' + path).yellow);
// 					});
// 				});
// 			}
// 		});
// 	});
// });