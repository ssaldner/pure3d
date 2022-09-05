import sys
import os
from flask import Flask, render_template, abort, make_response


BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = f"{BASE}/data/3d"
ROOT_URL = "/data/"
SCENE = "clanwilliam.json"
WIDTH = "600px"
HEIGHT = "600px"
STATUS = os.environ["PILOT_MODE"]

app = Flask(__name__, static_folder=f"{BASE}/static")


def debug(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


@app.route("/")
def index():
    return render_template("index.html", status=STATUS, scene=SCENE, height=HEIGHT, width=WIDTH)


@app.route("/voyager/<string:scene>")
def voyager(scene):
    ext = "min" if STATUS == "prod" else "dev"
    return render_template(
        "voyager.html",
        ext=ext,
        status=STATUS,
        root=ROOT_URL,
        scene=scene,
    )


@app.route("/data/<path:path>")
def data(path):
    dataPath = f"{DATA_DIR}/{path}"
    if not os.path.isfile(dataPath):
        debug(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)
