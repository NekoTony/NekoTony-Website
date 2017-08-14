import asyncio
from flask import Flask, render_template, url_for
import aiohttp
import os
import time
from htmlmin.minify import html_minify
from datetime import datetime, date

app = Flask(__name__)


#Flask Functions
@app.route('/')
def home():
    title = "{} | Home".format(username.upper())
    video = "True"
    return html_minify(render_template('index.html', title=title, video=video, desc=desc))

@app.route('/about')
def about():
    title = "{} | About".format(username.upper())
    video = "False"
    age = calculate_age(datetime.strptime('Aug 27 2000', '%b %d %Y'))
    return html_minify(render_template('about.html', title=title, video=video, desc=desc))

@app.route('/portfolio')
def portfolio():
    title = "{} | Portfolio".format(username.upper())
    video = "False"
    return html_minify(render_template('portfolio.html', title=title, video=video, desc=desc))

@app.route('/contact')
def contact():
    title = "{} | Contact".format(username.upper())
    video = "False"
    return html_minify(render_template('contact.html', title=title, video=video, desc=desc))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

#Regular Functions
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day)) #borrowed from stack overflow. Coudln't find a module to get age from date.

async def discord_name():
    global username
    url = 'https://discordapp.com/api/v7/users/180339602798804992'
    headers = {
    "Authorization" : "BotToken"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            try:
                username = data["username"]
            except:
                username = "NekoTony"

            return username

#Main Variables
username = ""
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)
username = loop.run_until_complete(discord_name())
desc = "Hello, I'm {} and welcome to http://NekoTony.pro/. This is my personal website, made by me. Enjoy! ".format(username)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)

