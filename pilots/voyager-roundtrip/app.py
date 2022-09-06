import os
import sys
from dispatcher import DispatcherMiddleware
from flask import Flask, request, render_template, abort, make_response
from webdavapp import app as webdavapp


BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = f"{BASE}/data/3d"
ROOT_URL = "/data/"
ROOT_URL_EDIT = "/webdav/"
SCENE = "clanwilliam.json"
WIDTH = "1000px"
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
    editable = request.args.get("edit", "0")
    editable = editable == "1"

    kind = "story" if editable else "explorer"
    patch = ".patch" if editable else ""
    # patch = ".debug" if editable else ""
    root = ROOT_URL_EDIT if editable else ROOT_URL

    return render_template(
        "voyager.html",
        ext=ext,
        root=root,
        scene=scene,
        kind=kind,
        patch=patch,
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


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/webdav/': webdavapp,
})
