import os
import random
import sys
import json
import utils

from collections import namedtuple
from flask import Flask, jsonify, send_from_directory, abort, send_file, render_template

# Checking if you have config.json on your API
try:
    with open("config.json", encoding='utf-8') as data:
        config = json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
except FileNotFoundError:
    print("You need to make a config file to be able to run this API")
    sys.exit()


app = Flask(__name__)

# Cache all images
cache_images = [img for img in os.listdir(config.imagefolder)]

# Check for changes in image folder
extra_dirs = [config.imagefolder, "templates"]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)


@app.route("/")
def index():
    return render_template(
        'index.html', config=config,
        background=random.choice(cache_images), images=len(cache_images)
    )


# This is just for the memes, the holy 418 error \o/
@app.route("/teapot")
@app.route("/418")
def teapot():
    return abort(418)


@app.route("/<filename>")
def coffee(filename):
    return send_from_directory(config.imagefolder, filename)


@app.route("/assets/images/<filename>")
def template_images(filename):
    return send_from_directory("templates/images", filename)


@app.route("/random")
def randomcoffee():
    choose_random = random.choice(cache_images)
    name = choose_random.split(".")

    return send_file(
        f"{config.imagefolder}/{choose_random}",
        mimetype=f"image/{name[1] if name[1] != 'jpg' else 'jpeg'}",
        attachment_filename=choose_random
    )


@app.route("/random.json")
def randomcoffeeJSON():
    domain = config.domain

    if config.localhost:
        domain = f"http://localhost:{config.port}/"

    return jsonify({
        "file": domain + random.choice(cache_images)
    })


if __name__ == '__main__':
    utils.randomize(config.imagefolder, config.suffix)
    app.run(port=config.port, debug=config.debug, extra_files=extra_files)
