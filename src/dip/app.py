from flask import Flask, render_template, url_for, abort, make_response
import os
import sys
import json
from markdown import markdown

from helpers.messages import Messages
from helpers.files import readFile, dirExists


# create and configure app
app = Flask(__name__)
app.secret_key = "dev"
title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D website"

# variables
BASE = os.path.expanduser("~/github/clariah/pure3d")
DATA_DIR = f"{BASE}/data"
EDITION_DIR = f"{DATA_DIR}/editions"

WIDTH = "600px"
HEIGHT = "600px"


# functions
def getEditionsList(M):
    # to get enumeration of top level directories
    # these are joined with the "edition" directory path to get
    # path of each edition
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


def dcReaderJSON(M, dcDir, dcFile):
    # to read different values from the Dublin core file
    pass


def debug(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


# app url routes start here


@app.route("/")
@app.route("/home")
# Display home page
def home():
    M = Messages(app)

    # display list of editions on home page
    # used "dc.title" from the Dublin Core metadata
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

        candy = f"editions/{i}/candy/icon.png"
    
        #display project logo as banner
        logo = url_for('data', path=candy)

        editionData[i] = dict(
            title=title,
            url=url, logo=logo
        )

    editionLinks = []  # to get url redirections of individual pages of each edition

    for (i, data) in sorted(editionData.items()):
        title = data["title"]
        url = data["url"]
        logo = data["logo"]
        editionLinks.append(
            f"""
            <img src="{logo}">
            <a href="{url}">{title}</a><br>
        """
        )

    editionLinks = "\n".join(editionLinks)

    return render_template(
        "index.html",
        url=url, title=title,
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

    homeUrl = url_for("edition_page", editionN=editionN)
    bgUrl = url_for("editionBackground", editionN=editionN)

    return render_template(
        "editionTexts.html",
        text=aboutHtml,
        homeUrl=homeUrl,
        bgUrl=bgUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:editionN>/<int:modelN>")
# Display page for individual models in an edition
def model_page(editionN, modelN):
    M = Messages(app)

    md = f"{EDITION_DIR}/{editionN}/3d/{modelN}"  # model directory on filesystem
    root = f"data/editions/{editionN}/3d/{modelN}/"  # model root url

    candyLogo = f"editions/{editionN}/candy/logo.png"
    
    #display project logo as banner
    logo = url_for('data', path=candyLogo)

    # render About information
    aboutFile = "about.md"
    aboutHtml = render_md(M, md, aboutFile)

    # urls for different tabs on the edition page
    homeUrl = url_for("edition_page", editionN=editionN)
    aboutUrl = url_for("editionAbout", editionN=editionN)
    bgUrl = url_for("editionBackground", editionN=editionN)

    # displaying 3d models
    # accesses the scene file
    for file in os.listdir(md):
        if file.endswith(".json"):
            scene = file
    

    return render_template(
        "model.html",
        aboutHtml=aboutHtml,
        editionN=editionN,
        modelN=modelN,
        scene=scene,
        height=HEIGHT,
        width=WIDTH,
        homeUrl=homeUrl,
        aboutUrl=aboutUrl,
        bgUrl=bgUrl,
        root=root,
        logo=logo,
        messages=M.generateMessages(),
    )


@app.route("/voyager/<string:scene>/<path:root>")
def voyager(scene, root):
    # url for voyager in explorer mode
    M = Messages(app)
    ext = "min"
    root = f"/{root}"

    return render_template(
        "voyager.html", ext=ext, root=root, scene=scene, messages=M.generateMessages()
    )

@app.route("/data/<path:path>")
def data(path):
    # url accesing data from the editions
    dataPath = f"{DATA_DIR}/{path}"
    if not os.path.isfile(dataPath):
        debug(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)


@app.route("/<int:editionN>")
# Display for editions page(s)
def edition_page(editionN):
    M = Messages(app)

    ed = f"{EDITION_DIR}/{editionN}"
    candyLogo = f"editions/{editionN}/candy/logo.png"

    #display title
    jsonDir = f"{EDITION_DIR}/{editionN}/meta"
    jsonFile = "dc.json"
    fh = readFile(jsonDir, jsonFile)
    if type(fh) is str:
        M.addMessage("error", fh)
        dcJson = {}
    else:
        dcJson = json.load(fh)

    if "dc.title" in dcJson:
        ed_title = dcJson["dc.title"]
    else:
        M.addMessage("warning", "No 'dc.title' in Dublin Core metadata")
        ed_title = "No title"
    
    #display project logo as banner
    logo = url_for('data', path=candyLogo)

    
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
        candyIcon = f"editions/{editionN}/3d/{j}/candy/icon.png"
        icon = url_for('data', path=candyIcon)
        modelData[j] = dict(
            title=title,
            url=url,icon=icon
        )


    modelLinks = []

    for (i, data) in sorted(modelData.items()):
        title = data["title"]
        url = data["url"]
        icon = data["icon"]
        modelLinks.append(
            f"""
            <img src="{icon}" alt="model icon">
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
        logo=logo,icon=icon,
        ed_title=ed_title,
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
    homeUrl = url_for("edition_page", editionN=editionN)

    return render_template(
        "editionTexts.html",
        text=backgroundHtml,
        homeUrl=homeUrl,
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
