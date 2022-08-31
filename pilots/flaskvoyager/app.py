import sys
import os
from flask import Flask, render_template, abort, make_response

app = Flask(__name__)

BASE = os.path.dirname(__file__)
DATA_DIR = f"{BASE}/data"
ROOT_URL = "/data/editions/1/3d/4/"
SCENE = "clanwilliam.json"
HEIGHT = "800px"


def debug(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


@app.route("/")
def index():
    return render_template("index.html")


def fillTemplate(name, status):
    style = f"display: block; position: relative; height: {HEIGHT};"
    ext = "min" if status else "dev"
    return render_template(f"{name}.html", ext=ext, style=style, root=ROOT_URL, scene=SCENE)


@app.route("/dip/prod")
def dipprod():
    return fillTemplate("dip", True)


@app.route("/dip/dev")
def dipdev():
    return fillTemplate("dip", False)


@app.route("/sip/prod")
def sipprod():
    return fillTemplate("sip", True)


@app.route("/sip/dev")
def sipdev():
    return fillTemplate("sip", False)


@app.route("/data/<path:path>")
def data(path):
    dataPath = f"{DATA_DIR}/{path}"
    if not os.path.isfile(dataPath):
        debug(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)
