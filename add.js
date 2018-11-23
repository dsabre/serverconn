#!/usr/bin/env node

const prompts = require('prompts');
const fs      = require('file-system');
const index   = require('./index');

const NEW_CATEGORY = '!!!new!!!';

module.exports.addServer = function(){
	index.getServersPath().then(serversPath =>{
		index.getUsername().then(username =>{
			fs.readFile(serversPath, (err, res) =>{
				let content = !err ? JSON.parse(res.toString()) : {};
				
				const categories      = Object.keys(content);
				let categoriesChoices = [{
					title : 'New',
					value : NEW_CATEGORY
				}];
				for(let i = 0; i < categories.length; i++){
					categoriesChoices.push({
						title : categories[i],
						value : categories[i]
					});
				}
				
				let questions = [
					{
						type    : 'text',
						name    : 'host',
						message : 'Host',
					},
					{
						type    : 'text',
						name    : 'username',
						message : 'Username',
						initial: username
					},
					{
						type    : 'text',
						style   : 'password',
						name    : 'password',
						message : 'Password'
					},
					{
						type    : 'select',
						name    : 'category',
						message : 'Category',
						choices : categoriesChoices
					},
					{
						type     : prev => prev === NEW_CATEGORY ? 'text' : null,
						name     : 'newCategory',
						message  : 'New category',
						validate : value => value !== '' ? true : 'Category is required'
					}
				];
				
				console.log('Add server:');
				prompts(questions).then(answers =>{
					const category = answers.category !== NEW_CATEGORY ? answers.category : answers.newCategory;
					
					if(!category){
						return;
					}
					
					if(Object.keys(content).indexOf(category) === -1){
						content[category] = [];
					}
					
					content[category].push({
						host     : answers.host,
						username : answers.username || username,
						password : answers.password,
						port     : 22
					});
					
					fs.writeFile(serversPath, JSON.stringify(content, null, 4));
				});
			});
		});
	});
};
