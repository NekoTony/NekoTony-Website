#!/usr/bin/env python3
# encoding: utf-8
import discord
import asyncio
from flask import Flask, render_template, url_for
import aiohttp
import os
import time
from htmlmin.minify import html_minify
from multiprocessing import Process, Value
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

app = Flask(__name__)
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)


async def discord_name():
    global username
    token = ""
    url = 'https://discordapp.com/api/v7/users/180339602798804992'
    headers = {}
    headers["Authorization"] = token
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            try:
                username = data["username"]
            except:
                username = "NekoTony"

            return username

@app.route('/')
def home():
    title = "{} | Home".format(username.upper())
    video = "True"
    return html_minify(render_template('index.html', title=title, video=video))

@app.route('/about')
def about():
    title = "{} | About".format(username.upper())
    video = "False"
    return html_minify(render_template('about.html', title=title, video=video))


@app.route('/portfolio')
def portfolio():
    title = "{} | Portfolio".format(username.upper())
    video = "False"
    return html_minify(render_template('portfolio.html', title=title, video=video))

@app.route('/contact')
def contact():
    title = "{} | Contact".format(username.upper())
    video = "False"
    return html_minify(render_template('contact.html', title=title, video=video))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    username = loop.run_until_complete(discord_name())
    app.run(debug=True, host='0.0.0.0', port=9000)
