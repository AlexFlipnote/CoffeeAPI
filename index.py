import os
import random
import sys
import json
import utils

from collections import namedtuple
from flask import Flask, jsonify, send_from_directory, abort, send_file, render_template

app = Flask(__name__)

# Checking if you have config.json on your API
try:
    with open("config.json", encoding='utf-8') as data:
        config = json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
except FileNotFoundError:
    print("You need to make a config file to be able to run this API")
    sys.exit()


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
    choose_random = random.choice([x for x in os.listdir(config.imagefolder)])
    return render_template('index.html', config=config, background=choose_random)


@app.route("/teapot")
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
    choose_random = random.choice([x for x in os.listdir(config.imagefolder)])
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

    choose_random = random.choice([x for x in os.listdir(config.imagefolder)])
    return jsonify({
        "file": domain + choose_random
    })


if __name__ == '__main__':
    utils.randomize(config.imagefolder, config.suffix)
    # Flask rest stuff
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=config.port, debug=config.debug, extra_files=extra_files)
