#!/usr/bin/env node

const index        = require('./index');
const openInEditor = require('open-in-editor');
const prompts      = require('prompts');
require('colors');

index.getServersPath().then(path =>{
	index.getConfig().then(config => {
		const choices = [
			{
				title : 'Sublime',
				value : 'sublime'
			},
			{
				title : 'Atom',
				value : 'atom'
			},
			{
				title : 'Webstorm',
				value : 'webstorm'
			},
			{
				title : 'Phpstorm',
				value : 'phpstorm'
			},
			{
				title : 'Vim',
				value : 'vim'
			}
		];
		
		let initial = 0;
		if(config.defaultEditor){
			for(initial; initial < choices.length; initial++){
				if(choices[initial].value === 'atom'){
					break;
				}
			}
		}
		
		prompts({
			type    : 'select',
			name    : 'value',
			message : 'Select editor',
			choices : choices,
			initial : initial
		}).then(answers =>{
			if(answers.value){
				index.setConfig('defaultEditor', answers.value).then(newConfig => {
					const editor = openInEditor.configure({
						editor : answers.value
					}, function(err){
						console.error('Something went wrong: ' + err);
					});
					
					editor.open(path)
					.then(function(){
						console.log('Opening file with ' + answers.value + '...');
					}, function(err){
						console.error(('Something went wrong: ' + err).red);
					});
				});
			}
		});
	});
});