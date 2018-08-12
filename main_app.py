import sys, os, requests
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response

import httplib2
import simplejson as json

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def showFrontPage():
	print("Hello World, from Maruaders")
	return render_template('front_page.html')

@app.route('/projects/')
def showProjectsPage():
	marauders_api = 'https://api.github.com/orgs/Marauders-9998/repos'
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
	marauders_api_response = requests.get(marauders_api, headers = headers)
	#print('---> marauders_api_response:', marauders_api_response)
	repos = []
	if marauders_api_response.status_code == 200:
		repositories = marauders_api_response.json()
		#print('---> repositories:', repositories)
		for repository in repositories:
			repo = {}
			repo['id'] = repository['id']
			repo['name'] = repository['name']
			repo['url'] = repository['html_url']
			repo['issues'] = repository['open_issues_count']
			repo['forks'] = repository['forks_count']
			repo['desc'] = repository['description']
			repo['lang'] = repository['language']
			repo['issues_api_url'] = repository['issues_url'].split('{')[0]
			repo['commits_api_url'] = repository['commits_url'].split('{')[0] 
			repos.append(repo)
	else:
		response = make_response(json.dumps('Could not request Github'), marauders_api_response.status_code)
		response.headers['Content-Type'] = 'application/json'
		return response

	print(repos)

	return render_template('projects_page.html', repositories = repos[::-1])

@app.route('/blogs/')
def showBlogPage():
	return render_template('blog_page.html')

@app.route('/forum/')
def showForumPage():
	return render_template('forum_page.html')

@app.route('/new_blog/')
def showNewBlogPage():
	return render_template('new_blog_page.html')

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)