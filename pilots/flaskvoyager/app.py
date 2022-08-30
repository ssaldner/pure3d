import sys
import os
from flask import Flask, render_template, abort, make_response

app = Flask(__name__)

BASE = os.path.dirname(__file__)
dataDir = f"{BASE}/data"


def debug(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


@app.route("/")
def index():
    # see https://github.com/Smithsonian/dpo-voyager/issues/158
    rootUrl = "/data/editions/1/3d/4/"
    model = "clanwilliam.gltf"
    scene = "clanwilliam.json"
    height = "800px"

    style = f"display: block; position: relative; height: {height};"
    return render_template(
        "index.html", style=style, root=rootUrl, model=model, scene=scene
    )


@app.route("/data/<path:path>")
def data(path):
    dataPath = f"{dataDir}/{path}"
    if not os.path.isfile(dataPath):
        debug(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)
