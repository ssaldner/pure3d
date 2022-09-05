from flask import Flask, render_template


app2 = Flask(__name__)


@app2.route("/<path:path>")
def index(path):
    return render_template("index.html", theApp="app2", path=path)
