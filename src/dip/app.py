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


def getEditionsList(M):
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


def getModelDir(M):
    editions = getEditionsList(M)
    for e in editions:
        modelDir = f"{editionDir}/{e}/3d"
        return modelDir


def getModelsList(M):
    # to get enumeration of sub-directories under folder "3d"
    modelns = []
    dir = getModelDir(M)
    with os.scandir(dir) as md:
        for model in md:
            if model.is_dir():
                name = model.name
                if name.isdigit():
                    modelns.append(int(name))
    return sorted(modelns)


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

    editionNumbers = getEditionsList(M)

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
        "editionTexts.html",
        text=aboutHtml,
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

    Dir = f"{editionDir}/{editionN}"
    introFile = "intro.md"
    usageFile = "usage.md"

    introHtml = render_md(M, Dir, introFile)
    usageHtml = render_md(M, Dir, usageFile)

    aboutUrl = url_for("editionAbout", editionN=editionN)
    bgUrl = url_for("editionBackground", editionN=editionN)

    modelNumbers = getModelsList(M)
    modelData = {}

    for j in modelNumbers:
        modelDir = f"{Dir}/3d/{j}"
        modelFile = "title.txt"
        nameFile = os.path.join(modelDir, modelFile)
        with open(nameFile) as f:
            title = f.read()

        url = f"""/{j}"""
        modelData[j] = dict(
            title=title,
            url=url,
        )

    modelLinks = []

    for (i, data) in sorted(modelData.items()):
        title = data["title"]
        url = data["url"]
        modelLinks.append(
            f"""
            <a href="{url}">{title}</a><br>
        """
        )

    modelLinks = "\n".join(modelLinks)

    return render_template(
        "edition.html",
        usage=usageHtml,
        intro=introHtml,
        editioN=editionN,
        aboutUrl=aboutUrl,
        bgUrl=bgUrl,
        modelLinks=modelLinks,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>/project_background")
# Display about page for specific edition
def editionBackground(editionN):
    M = Messages(app)
    Dir = f"{editionDir}/{editionN}"
    backgroundFile = "description.md"
    backgroundHtml = render_md(M, Dir, backgroundFile)

    return render_template(
        "editionTexts.html",
        text=backgroundHtml,
        editionN=editionN,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>/sources")
# Display about page for specific edition
def editionSources(editionN):
    # M = Messages(app)
    pass


if __name__ == "__main__":
    app.run()
