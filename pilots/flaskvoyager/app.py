from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    model = "here comes a model"
    return render_template("index.html", model=model)
