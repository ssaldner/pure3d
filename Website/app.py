from flask import Flask, render_template  # for flask
import os
import json
from markdown import markdown

# create and configure app
app = Flask(__name__)
title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D website"

# variables
dataDir = "./data/editions"
editions = next(os.walk(dataDir))[1]

# functions


def editionsList():  # to get paths/enumeration of edition (top level) directories
    editionDir = []
    #editionN = []
    for local_folder in editions:
        editionDir.append(os.path.abspath(os.path.join(dataDir, local_folder)))

    #for (n, e) in enumerate(editionDir):
        #editionN.append(n + 1)  # edition number

    return editionDir  #, editionN  # edition directory path, edition number


def render_md(mdPath, mdFile):  # to render markdown files
    filename = f"{mdPath}/texts/{mdFile}"
    with open(filename, 'r') as f:
        text = f.read()
        html = markdown(text)
        return html

# app url routes start here

@app.route("/")
@app.route("/home")
# Display home page
def home():
    editionDir = editionsList()  

    title = []
    url = []

    for i in editionDir: 
        with open((f"{i}/meta/dc.json"), "r") as dcFile:
            dcJson = json.load(dcFile)
            title.append(dcJson["dc.title"])

    for (n, e) in enumerate(title):
        editionN = n+1
        url.append(f"""<a href="/{editionN}">{e}</a>""")
    return render_template("index.html", url=url, editionN=editionN)


@app.route("/about")
# Display the About page
def about():
    return render_template('about.html')


# Display for editions page(s)
@app.route("/<int:editionN>")
def edition_page(editionN):
    editionDir = editionsList()
    for (n, e) in enumerate(editionDir):
        editionN = n+1
        intro = render_md(e, "intro.md")
    return render_template("edition.html", intro=intro), editionN


if __name__ == "__main__":
    app.run()