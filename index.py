import os
import random
import json
import renamer

from collections import namedtuple
from flask import Flask, jsonify, send_from_directory, abort, send_file

app = Flask(__name__)

with open("config.json") as data:
    config = json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


@app.route("/")
def index():
    return "It works ☕"


@app.route("/teapot")
def teapot():
    return abort(418)


@app.route("/<filename>")
def coffee(filename):
    return send_from_directory(config.imagefolder, filename)


@app.route("/random")
def randomcoffee():
    choose_random = random.choice([x for x in os.listdir(config.imagefolder)])
    name = choose_random.split(".")
    return send_file(
        f"{config.imagefolder}/{choose_random}",
        mimetype="image/png",
        attachment_filename=f".{name[1]}"
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


renamer.randomize(config.imagefolder, config.suffix)
app.run(port=config.port, debug=config.debug)
