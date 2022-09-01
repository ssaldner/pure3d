import sys
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, render_template, abort, make_response
from webdavapp import app as webdavapp


BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = f"{BASE}/data/3d"
ROOT_URL = "/data/"
SCENE = "clanwilliam.json"
HEIGHT = "800px"
STATUS = os.environ["PILOT_MODE"]

app = Flask(__name__)


def debug(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


def fillTemplate(name):
    style = f"display: block; position: relative; height: {HEIGHT};"
    ext = "min" if STATUS == "prod" else "dev"
    return render_template(
        f"{name}.html", ext=ext, status=STATUS, style=style, root=ROOT_URL, scene=SCENE
    )


@app.route("/")
def index():
    return fillTemplate("index")


@app.route("/dataw/<path:path>")
def dataw(path):
    dataPath = f"{DATA_DIR}/{path}"
    if not os.path.isfile(dataPath):
        debug(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/data': webdavapp,
})
