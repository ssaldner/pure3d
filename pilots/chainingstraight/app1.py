from flask import Flask, render_template


app1 = Flask(__name__)


@app1.route("/<path:path>")
def index(path):
    return render_template("index.html", theApp="app1", path=path)
