from app1 import app1
from app2 import app2
from flask import Flask, render_template
from dispatcher import DispatcherMiddleware


app = Flask(__name__)


@app.route("/")
@app.route("/<path:path>")
def index(path="/"):
    return render_template("index.html", theApp="the main app", path=path)


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/app1': app1,
    '/app2': app2,
})
