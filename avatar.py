import discord
import asyncio
from flask import Flask, render_template
import aiohttp
import time
from multiprocessing import Process, Value
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps
from datetime import datetime

avatar_data = []
id = "180339602798804992"
url = 'https://discordapp.com/api/v7/users/{}'.format(id)
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)
token = ""


async def avatarz(token):
    headers = {}
    headers["Authorization"] = token
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            try:
                avatar_data = ["{}".format(data["avatar"])]
            except:
                print("Error getting avatar..")

    avatarlink = avatar_url(id, avatar_data[0])
    async with aiohttp.ClientSession() as ses, ses.get(avatarlink) as r:
        ava = await r.read()

    with open('static/avatar.png', 'wb') as f:
        print("Saved avatar!!")
        f.write(ava)


def avatar_url(id, avatar):
    url = 'https://cdn.discordapp.com/avatars/{}/{}.png?size=1024'.format(
        id, avatar)
    return url


if __name__ == '__main__':
    while True:
        avatar = loop.run_until_complete(avatarz(token))
        print(str(datetime.now()))
        time.sleep(3600)
