import os
import sys
import json
import random
import secrets

from collections import namedtuple
from quart import Quart, jsonify, send_from_directory, send_file, render_template

# Checking if you have config.json on your API
try:
    with open("config.json", encoding='utf-8') as data:
        config = json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
except FileNotFoundError:
    print("You need to make a config file to be able to run this API")
    sys.exit()


app = Quart(__name__)

# Cache all images
cache_images = [img for img in os.listdir(config.imagefolder)]


def randomize(dir, checker):
    """ Scout the images folder and giving token names to files missing """
    for file in os.listdir(dir):
        name = file.split(".")
        if not name[0].endswith(checker):
            os.rename(f"{dir}/{file}", f"{dir}/{secrets.token_urlsafe(8)}{checker}.{name[-1]}")


@app.route("/")
async def index():
    return await render_template(
        'index.html', config=config,
        background=random.choice(cache_images), images=len(cache_images)
    )


# This is just for the memes, the holy 418 error \o/
@app.route("/teapot")
@app.route("/418")
async def teapot():
    return await render_template("418.html"), 418


@app.route("/<filename>")
async def coffee(filename):
    return await send_from_directory(config.imagefolder, filename)


@app.route("/assets/<filename>")
async def template_images(filename):
    return await send_from_directory("templates/assets", filename)


@app.route("/random")
async def randomcoffee():
    choose_random = random.choice(cache_images)
    name = choose_random.split(".")

    return await send_file(
        f"{config.imagefolder}/{choose_random}",
        mimetype=f"image/{name[-1] if name[-1] != 'jpg' else 'jpeg'}",
        attachment_filename=choose_random
    )


@app.route("/random.json")
async def randomcoffeeJSON():
    return jsonify({
        "file": config.domain + random.choice(cache_images)
    })


randomize(config.imagefolder, config.suffix)
app.run(port=config.port, debug=config.debug)
