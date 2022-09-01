import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, render_template
from webdavapp import app as webdavapp


ROOT_URL = "/data/"
SCENE = "clanwilliam.json"
HEIGHT = "800px"
STATUS = os.environ["PILOT_MODE"]

app = Flask(__name__)


def fillTemplate(name):
    style = f"display: block; position: relative; height: {HEIGHT};"
    ext = "min" if STATUS == "prod" else "dev"
    return render_template(
        f"{name}.html", ext=ext, status=STATUS, style=style, root=ROOT_URL, scene=SCENE
    )


@app.route("/")
def index():
    return fillTemplate("index")


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/data': webdavapp,
})
