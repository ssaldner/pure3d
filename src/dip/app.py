from flask import Flask, render_template, url_for
import os
import json
from markdown import markdown

from helpers.messages import Messages
from helpers.files import readFile, dirExists


# create and configure app
app = Flask(__name__)
title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D website"

# variables
BASE = os.path.expanduser("~/github/clariah/pure3d")
dataDir = f"{BASE}/data"
editionDir = f"{dataDir}/editions"


def editionsList(M):
    # to get enumeration of top level directories
    numbers = []

    if not dirExists(editionDir):
        M.addMessage("error", f"Edition directory {editionDir} does not exist")
        return numbers

    with os.scandir(editionDir) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


def modelsList(M):
    # to get enumeration of sub-directories under folder "3d"
    pass


def render_md(M, mdPath, mdFile):
    # to render markdown files
    fileDir = f"{mdPath}/texts"
    fh = readFile(fileDir, mdFile)
    if type(fh) is str:
        M.addMessage("error", fh)
        html = ""
    else:
        text = fh.read()
        html = markdown(text)
    return html


def dcReaderJSON(M):
    # to read different values from the Dublin core file
    pass


# app url routes start here


@app.route("/")
@app.route("/home")
# Display home page
def home():
    M = Messages(app)

    editionNumbers = editionsList(M)

    editionData = {}

    # just for testing

    for tp in ("debug", "info", "warning", "error"):
        M.addMessage(tp, f"This is a {tp} message")

    for i in editionNumbers:
        jsonDir = f"{editionDir}/{i}/meta"
        jsonFile = "dc.json"
        fh = readFile(jsonDir, jsonFile)
        if type(fh) is str:
            M.addMessage("error", fh)
            dcJson = {}
        else:
            dcJson = json.load(fh)

        if "dc.title" in dcJson:
            title = dcJson["dc.title"]
        else:
            M.addMessage("warning", "No 'dc.title' in Dublin Core metadata")
            title = "No title"
        url = f"""/{i}"""

        editionData[i] = dict(
            title=title,
            url=url,
        )

    editionLinks = []

    for (i, data) in sorted(editionData.items()):
        title = data["title"]
        url = data["url"]
        editionLinks.append(
            f"""
            <a href="{url}">{title}</a><br>
        """
        )

    editionLinks = "\n".join(editionLinks)

    return render_template(
        "index.html",
        url=url,
        editionLinks=editionLinks,
        messages=M.generateMessages(),
    )


@app.route("/about")
# Display the About page
def about():
    M = Messages(app)

    fileDir = f"{BASE}/src/dip"
    fileName = "about.md"
    fh = readFile(fileDir, fileName)
    if type(fh) is str:
        M.addMessage("error", fh)
        text = ""
    else:
        text = fh.read()

    html = markdown(text)

    return render_template(
        "about.html",
        about=html,
        messages=M.generateMessages(),
    )


@app.route("/supriseme")
def supriseme():
    # M = Messages(app)

    pass


@app.route("/contact")
def contact():
    # M = Messages(app)

    pass


@app.route("/<int:editionN>/about")
# Display about page for specific edition
def editionAbout(editionN):
    M = Messages(app)

    aboutDir = f"{editionDir}/{editionN}"
    aboutFile = "about.md"
    aboutHtml = render_md(M, aboutDir, aboutFile)

    return render_template(
        "about.html",
        about=aboutHtml,
        editionN=editionN,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>/<int:modelN>")
# Display page for individual models in an edition
def model_page(editionN, modelN):
    # M = Messages(app)

    pass


@app.route("/<int:editionN>")
# Display for editions page(s)
def edition_page(editionN):
    M = Messages(app)

    M.addMessage("debug", f"I am here {editionN=}")
    introDir = f"{editionDir}/{editionN}"
    introFile = "intro.md"

    introHtml = render_md(M, introDir, introFile)
    editionUrl = url_for("editionAbout", editionN=editionN)
    return render_template(
        "edition.html",
        intro=introHtml,
        editioN=editionN,
        editionUrl=editionUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>/project_background")
# Display about page for specific edition
def editionBackground(editionN):
    # M = Messages(app)
    pass


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
