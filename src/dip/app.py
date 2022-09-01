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
DATA_DIR = f"{BASE}/data"
EDITION_DIR = f"{DATA_DIR}/editions"


def getEditionsList(M):
    # to get enumeration of top level directories
    numbers = []

    if not dirExists(EDITION_DIR):
        M.addMessage("error", f"Edition directory {EDITION_DIR} does not exist")
        return numbers

    with os.scandir(EDITION_DIR) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


def getModelsList(M, editionN):
    # to get enumeration of sub-directories under folder "3d"
    modelns = []
    modelDir = f"{EDITION_DIR}/{editionN}/3d"
    with os.scandir(modelDir) as md:
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

    for i in editionNumbers:
        jsonDir = f"{EDITION_DIR}/{i}/meta"
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

    aboutDir = f"{EDITION_DIR}/{editionN}"
    aboutFile = "about.md"
    aboutHtml = render_md(M, aboutDir, aboutFile)

    bgUrl = url_for("editionBackground", editionN=editionN)

    return render_template(
        "editionTexts.html",
        text=aboutHtml,
        bgUrl=bgUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>/<int:modelN>")
# Display page for individual models in an edition
def model_page(editionN, modelN):
    M = Messages(app)

    md = f"{EDITION_DIR}/{editionN}/3d/{modelN}"

    # render about information
    aboutFile = "about.md"
    aboutHtml = render_md(M, md, aboutFile)

    # displaying 3d models
    

    return render_template(
        "model.html",
        aboutHtml=aboutHtml,
        editionN=editionN,
        modelN=modelN,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>")
# Display for editions page(s)
def edition_page(editionN):
    M = Messages(app)

    ed = f"{EDITION_DIR}/{editionN}"

    # rendering texts
    introFile = "intro.md"
    usageFile = "usage.md"

    introHtml = render_md(M, ed, introFile)
    usageHtml = render_md(M, ed, usageFile)

    # url variables for tabs on page
    aboutUrl = url_for("editionAbout", editionN=editionN)
    bgUrl = url_for("editionBackground", editionN=editionN)

    # hyper-linked models list
    modelNumbers = getModelsList(M, editionN)
    modelData = {}

    for j in modelNumbers:
        modelDir = f"{ed}/3d/{j}"
        modelFile = "title.txt"
        nameFile = os.path.join(modelDir, modelFile)
        with open(nameFile) as f:
            title = f.read()

        url = f"""/{editionN}/{j}"""
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
    ed = f"{EDITION_DIR}/{editionN}"
    backgroundFile = "description.md"
    backgroundHtml = render_md(M, ed, backgroundFile)

    aboutUrl = url_for("editionAbout", editionN=editionN)

    return render_template(
        "editionTexts.html",
        text=backgroundHtml,
        aboutUrl=aboutUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>/sources")
# Display about page for specific edition
def editionSources(editionN):
    # M = Messages(app)
    pass


if __name__ == "__main__":
    app.run()
