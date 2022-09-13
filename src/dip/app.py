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
PROJECT_DIR = f"{DATA_DIR}/projects"

WIDTH = "600px"
HEIGHT = "600px"


# functions
def getProjectsList(M):
    # to get enumeration of top level directories
    # these are joined with the "project" directory path to get
    # path of each project
    numbers = []

    if not dirExists(PROJECT_DIR):
        M.addMessage("error", f"Model directory {PROJECT_DIR} does not exist")
        return numbers

    with os.scandir(PROJECT_DIR) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


def getModelsList(M, projectN):
    # to get enumeration of sub-directories under folder "3d"
    modelns = []
    modelDir = f"{PROJECT_DIR}/{projectN}/3d"
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

    # display list of projects on home page
    # used "dc.title" from the Dublin Core metadata
    projectNumbers = getProjectsList(M)

    projectData = {}

    for i in projectNumbers:
        jsonDir = f"{PROJECT_DIR}/{i}/meta"
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

        candy = f"projects/{i}/candy/icon.png"
    
        #display project logo as banner
        logo = url_for('data', path=candy)

        projectData[i] = dict(
            title=title,
            url=url, logo=logo
        )

    projectLinks = []  # to get url redirections of individual pages of each project

    for (i, data) in sorted(projectData.items()):
        title = data["title"]
        url = data["url"]
        logo = data["logo"]
        projectLinks.append(
            f"""
            <img src="{logo}">
            <a href="{url}">{title}</a><br>
        """
        )

    projectLinks = "\n".join(projectLinks)

    return render_template(
        "index.html",
        url=url, title=title,
        projectLinks=projectLinks,
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


@app.route("/<int:projectN>/about")
# Display about page for specific project
def projectAbout(projectN):
    M = Messages(app)

    aboutDir = f"{PROJECT_DIR}/{projectN}"
    aboutFile = "about.md"
    aboutHtml = render_md(M, aboutDir, aboutFile)

    homeUrl = url_for("project_page", projectN=projectN)
    bgUrl = url_for("projectBackground", projectN=projectN)

    return render_template(
        "projectTexts.html",
        text=aboutHtml,
        homeUrl=homeUrl,
        bgUrl=bgUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:projectN>/<int:modelN>")
# Display page for individual models in an project
def model_page(projectN, modelN):
    M = Messages(app)

    md = f"{PROJECT_DIR}/{projectN}/3d/{modelN}"  # model directory on filesystem
    root = f"data/projects/{projectN}/3d/{modelN}/"  # model root url

    candyLogo = f"projects/{projectN}/candy/logo.png"
    
    #display project logo as banner
    logo = url_for('data', path=candyLogo)

    # render About information
    aboutFile = "about.md"
    aboutHtml = render_md(M, md, aboutFile)

    # urls for different tabs on the project page
    homeUrl = url_for("project_page", projectN=projectN)
    aboutUrl = url_for("projectAbout", projectN=projectN)
    bgUrl = url_for("projectBackground", projectN=projectN)

    # displaying 3d models
    # accesses the scene file
    for file in os.listdir(md):
        if file.endswith(".json"):
            scene = file
    

    return render_template(
        "model.html",
        aboutHtml=aboutHtml,
        projectN=projectN,
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
    # url accesing data from the projects
    dataPath = f"{DATA_DIR}/{path}"
    if not os.path.isfile(dataPath):
        debug(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)


@app.route("/<int:projectN>")
# Display for projects page(s)
def project_page(projectN):
    M = Messages(app)

    ed = f"{PROJECT_DIR}/{projectN}"
    candyLogo = f"projects/{projectN}/candy/logo.png"

    #display title
    jsonDir = f"{PROJECT_DIR}/{projectN}/meta"
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
    aboutUrl = url_for("projectAbout", projectN=projectN)
    bgUrl = url_for("projectBackground", projectN=projectN)

    # hyper-linked models list
    modelNumbers = getModelsList(M, projectN)
    modelData = {}

    for j in modelNumbers:
        modelDir = f"{ed}/3d/{j}"
        modelFile = "title.txt"
        nameFile = os.path.join(modelDir, modelFile)
        with open(nameFile) as f:
            title = f.read()

        url = f"""/{projectN}/{j}"""
        candyIcon = f"projects/{projectN}/3d/{j}/candy/icon.png"
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
        "project.html",
        usage=usageHtml,
        intro=introHtml,
        editioN=projectN,
        aboutUrl=aboutUrl,
        bgUrl=bgUrl,
        modelLinks=modelLinks,
        logo=logo,icon=icon,
        ed_title=ed_title,
        messages=M.generateMessages(),
    )


@app.route("/<int:projectN>/project_background")
# Display about page for specific project
def projectBackground(projectN):
    M = Messages(app)
    ed = f"{PROJECT_DIR}/{projectN}"
    backgroundFile = "description.md"
    backgroundHtml = render_md(M, ed, backgroundFile)

    aboutUrl = url_for("projectAbout", projectN=projectN)
    homeUrl = url_for("project_page", projectN=projectN)

    return render_template(
        "projectTexts.html",
        text=backgroundHtml,
        homeUrl=homeUrl,
        aboutUrl=aboutUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:projectN>/sources")
# Display about page for specific project
def projectSources(projectN):
    # M = Messages(app)
    pass


if __name__ == "__main__":
    app.run()
