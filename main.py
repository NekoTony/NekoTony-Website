from flask import Flask, render_template, url_for, request, flash, Markup, redirect, Response, send_from_directory, jsonify
import flask
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageChops, ImageFilter
import requests
import os.path
import os
from bs4 import BeautifulSoup
import time
from htmlmin.minify import html_minify
from datetime import datetime, date
import textwrap
from random import choice, sample, randint
from flask_cors import CORS
from functools import wraps
import acnl as belltree
from os.path import splitext
from datetime import time as t

app = Flask(__name__, static_folder='static', static_url_path='/static')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def shadowcolor(color):
    color = color.lstrip("#")
    rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    n1 = rgb[0] - percentage(80, rgb[0])
    n2 = rgb[1] - percentage(80, rgb[1])
    n3 = rgb[2] - percentage(80, rgb[2])
    rgb = (int(round(n1)), int(round(n2)), int(round(n3)))
    return '#%02x%02x%02x' % rgb


def percentage(percent, whole):
    return (percent * whole) / 100


def tbtsig(path):
    img = Image.open(choice(("acnlimg/antonio/img1.png", "acnlimg/antonio/img2.png", "acnlimg/antonio/img3.png",
                             "acnlimg/antonio/img4.png"))).convert("RGBA").resize((715, 190), Image.ANTIALIAS)
    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(tmp)
    draw.rectangle(((20, 20), (img.size[0] - 20, img.size[1] - 20)),
                   fill=(0, 0, 0, 140), outline=(0, 0, 0, 190))
    W, H = img.size
    font2 = ImageFont.truetype("static/FinkHeavy.ttf", 50)
    font = ImageFont.truetype("static/FinkHeavy.ttf", 72)
    w, h = draw.textsize("Antonio", font)
    draw.text(((W-w)/2, ((H-h)/2) - 30), "Antonio", fill="white", font=font)
    MAX_W, MAX_H = (img.size[0] - 20, img.size[1] - 20)
    current_h, pad = 115, 10
    for x in textwrap.wrap("DA: 4B00-00BE-9524", width=50):
        w, h = draw.textsize(x, font=font2)
        draw.text(((MAX_W - w) / 2, current_h), x, font=font2)
        current_h += h + pad
    final = Image.alpha_composite(Image.new("RGBA", img.size), img)
    img.load()
    final = Image.alpha_composite(final, tmp)
    tmp.load()
    final.save(path, 'PNG', quality=100)
    final.load()
    return True


def katezilla(path):
    k = datetime.now().time()
    m, t = which_image(k)
    the = "static/" + t
    k = k.strftime("%-I:%M%p") + " EST"
    img = Image.new('RGBA', (700, 200), (0, 0, 0, 0))
    bg = Image.open(the).convert("RGBA")
    w, h = img.size
    basewidth = int(750 * bg.size[0] / bg.size[1])
    if basewidth <= 0:
        basewidth = 1
    bg = bg.resize((basewidth, 750), Image.ANTIALIAS)
    bg_w, bg_h = bg.size
    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            bg = Image.eval(bg, lambda x: x+(i+j)/1000)
            img.paste(bg, (i, j))
    draw = ImageDraw.Draw(img)
    font, font2, font3 = (ImageFont.truetype("static/FinkHeavy.ttf", 70), ImageFont.truetype(
        "static/FinkHeavy.ttf", 26), ImageFont.truetype("static/FinkHeavy.ttf", 30))
    W, H = draw.textsize("Switch: 2124-9321-8438", font)
    for x, y, z in (("Kate of Windfall", font, (175, 20)), ("Switch: 2124-9321-8438", font2, (175, 140)), (k, font3, (380, 90)), ("3DS: 2681-4644-1779", font2, (W - 220, 140))):
        draw.text(z, x, font=y)
    dk = Image.open("acnlimg/katezilla/duck.png").convert("RGBA")
    dk = dk.resize((int(200 * dk.size[0] / dk.size[1]), 200), Image.ANTIALIAS)
    img.paste(dk, (0, 10), dk)
    img.save(path, 'PNG', quality=100)
    img.load()
    dk.load()
    bg.load()
    return True


def clock(path):
    img = Image.new('RGBA', (550, 250), (0, 0, 0, 0))
    bg = Image.open(the).convert("RGBA")
    w, h = img.size
    hsize = 850
    basewidth = int(hsize * bg.size[0] / bg.size[1])
    if basewidth <= 0:
        basewidth = 1
    bg = bg.resize((basewidth, hsize), Image.ANTIALIAS)
    bg_w, bg_h = bg.size
    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            bg = Image.eval(bg, lambda x: x+(i+j)/1000)
            img.paste(bg, (i, j))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/FinkHeavy.ttf", 72)
    font2 = ImageFont.truetype("static/FinkHeavy.ttf", 20)
    W, H = draw.textsize(str(k), font)
    draw.text(((w-W)/2, ((h-H)/2 - 50)), str(k), fill="white", font=font)
    MAX_W, MAX_H = (img.size[0] - 20, img.size[1] - 20)
    current_h, pad = 130, 10
    for x in textwrap.wrap("Live time clock made by Antonio. Includes background changes depending on time of day.    It's {}!".format(m), width=50):
        w, h = draw.textsize(x, font=font2)
        draw.text(((MAX_W - w) / 2, current_h), x, font=font2)
        current_h += h + pad
    img.save(path, 'PNG', quality=100)
    img.load()
    bg.load()
    return True


def draw_rectangle(draw, coordinates, color, width=1):
    for i in range(width):
        rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
        rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
        draw.rectangle((rect_start, rect_end), outline=color)
        return draw


def in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:
        return start <= now or now < end


def which_image(current):
    if in_between(current, t(5), t(7)):
        return "Sunrise", "sky-6.png"
    elif in_between(current, t(17), t(18)):
        return "Sunset", "sky-2.png"
    elif in_between(current, t(8), t(16)):
        return "Daytime", "sky.png"
    elif in_between(current, t(16), t(17)):
        return "Daytime", "sky-1.png"
    elif in_between(current, t(18), t(21)):
        return "Nightime", "sky-3.png"
    elif in_between(current, t(21), t(3)):
        return "Late at night", "sky-4.png"
    elif in_between(current, t(3), t(5)):
        return "Dawn", "sky-5.png"


def get_spaced_colors(n):
    max_value = 16581375  # 255**3
    interval = int(max_value / n)
    colors = tuple(hex(I)[2:].zfill(6) for I in range(0, max_value, interval))
    return tuple((int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16), 140) for i in colors)


def banner(path):
    img = Image.new('RGBA', (715, 210), (0, 0, 0, 0))
    color = choice(get_spaced_colors(randint(23, 120)))
    draw = ImageDraw.Draw(img)
    draw.rectangle(((20, 20), (img.size[0] - 20, img.size[1] - 20)),
                   fill=color)
    W, H = img.size
    font2 = ImageFont.truetype("static/FinkHeavy.ttf", 54)
    font = ImageFont.truetype("static/FinkHeavy.ttf", 72)
    w, h = draw.textsize("Antonio's Garage", font)
    draw.text(((W-w)/2, ((H-h)/2) - 30),
              "Antonio's Garage", fill="white", font=font)
    MAX_W, MAX_H = (img.size[0] - 20, img.size[1] - 20)
    current_h, pad = 115, 10
    for x in textwrap.wrap("Opened - 10tbt per image", width=50):
        w, h = draw.textsize(x, font=font2)
        draw.text(((MAX_W - w) / 2, current_h), x, font=font2)
        current_h += h + pad
    img.save(path, 'PNG', quality=100)
    img.load()
    return True


@app.route('/deb/<path:path>')
def send_js(path):
    return send_from_directory('deb', path)


@app.route('/')
def home():
    return html_minify(render_template('index.html', title="{} | Home".format(username.upper()), video="False", desc=desc))


@app.route('/about')
def about():
    br = Markup("<br><br>")
    favshows = choice(["Doctor Who", "The Magicians", "Big Bang Theroy", "Golden Girls",
                       "Roseanne", "American Horror Story", "The Pokemon Series", "We Bare Bears"]).title()
    colors = choice(["Black", "White"]).title()
    nicknames = choice(["Big Ton", "Tont", "Tony", "Tony", "Tony", "NekoTony"])
    socialmedias = choice(['<b>Instagram:&nbsp;</b><a href="https://www.instagram.com/nerdietony/"> NerdieTony</a>',
                           '<b>Twitter:&nbsp;</b><a href="https://www.twitter.com/nerdietony/"> NerdieTony</a>', '<b>Discord:&nbsp;</b> {}#0047'.format(username)])
    return html_minify(render_template('about.html', title="{} | About".format(username.upper()), video="False", desc=desc, show=favshows, age=calculate_age(datetime.strptime('Aug 27 2000', '%b %d %Y')), br=br, color=colors, nick=nicknames, social=Markup(socialmedias)))


@app.route('/portfolio')
def portfolio():
    return html_minify(render_template('portfolio.html', title="{} | Portfolio".format(username.upper()), video="False", desc=desc))


@app.route("/tbt/<path:path>")
def acnlsignatures(path):
    time.sleep(0.3)
    fullpath = "/home/tmp/" + path
    if path == "valzed.png":
        o = belltree.valzed_sig(fullpath)
    elif path == "tbtsig.png":
        o = tbtsig(fullpath)
    elif path == "banner.png":
        o = banner(fullpath)
    elif path == "clock.png":
        o = clock(fullpath)
    elif path == "duck.png":
        o = katezilla(fullpath)
    else:
        return render_template('404.html'), 404

    k = open(fullpath, "rb").read()
    resp = flask.make_response(k)
    filename, ext = splitext(path)

    if ext.lower() == ".png":
        resp.content_type = "image/png"
    elif ext.lower() in (".jpeg", ".jpg"):
        resp.content_type = "image/jpeg"
    elif ext.lower() == ".gif":
        resp.content_type = "image/gif"
    else:
        resp.content_type = "image/png"

    os.remove(fullpath)
    return resp


@app.route('/contact')
def contact():
    return html_minify(render_template('contact.html', title="{} | Contact".format(username).upper(), video="False", desc=desc))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


username = 'Nekotony'
desc = "Wowie! Loook at this, I have a website! Isn't it cute? Anyways, this is the personal of Antonio Vallez but you can call me {}. Look around, have a few drinks, and remember...meow meow meow (=^-Ï‰-^=). <3".format(
    username)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000, threaded=True)
