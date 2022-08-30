from flask import Flask, render_template, url_for
import os
import json
from markdown import markdown

# create and configure app
app = Flask(__name__)
title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D website"

# variables
BASE = os.path.expanduser("~/github/clariah/pure3d")
dataDir = f"{BASE}/data"
editionDir = f"{dataDir}/editions"
MESSAGES = []


# functions
def clearMessages():
    MESSAGES.clear()


def addMessage(type, message):
    clearMessages()
    MESSAGES.append((type, message))


def generateMessages():
    html = []
    for (type, message) in MESSAGES:
        html.append(f"""<p class="type">{message}</p>""")
    return "\n".join(html)


def editionsList():
    # to get enumeration of top level directories
    numbers = []
    with os.scandir(editionDir) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


def modelsList():
    # to get enumeration of sub-directories under folder "3d"
    pass


def render_md(mdPath, mdFile):
    # to render markdown files
    filename = f"{mdPath}/texts/{mdFile}"
    with open(filename, "r") as f:
        text = f.read()
        html = markdown(text)
        return html


def dcReaderJSON():
    # to read different values from the Dublin core file
    pass


# app url routes start here


@app.route("/")
@app.route("/home")
# Display home page
def home():
    editionNumbers = editionsList()

    editionData = {}

    for i in editionNumbers:
        jsonFile = f"{editionDir}/{i}/meta/dc.json"
        with open(jsonFile, "r") as dcFile:
            dcJson = json.load(dcFile)
        title = dcJson["dc.title"]
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

    return render_template("index.html", url=url, editionLinks=editionLinks)


@app.route("/about")
# Display the About page
def about():
    filename = f"{BASE}/src/dip/about.md"
    with open(filename, "r") as f:
        text = f.read()
        html = markdown(text)
    return render_template("about.html", about=html)


@app.route("/supriseme")
def supriseme():
    pass


@app.route("/contact")
def contact():
    pass


@app.route("/<int:editionN>")
# Display for editions page(s)
def edition_page(editionN):
    addMessage("info", f"I am here {editionN=}")
    introDir = f"{editionDir}/{editionN}"
    introFile = "intro.md"
    introHtml = render_md(introDir, introFile)
    editionUrl = url_for("editionAbout", editionN=editionN)
    return render_template(
        "edition.html",
        intro=introHtml,
        editioN=editionN,
        editionUrl=editionUrl,
        messages=generateMessages(),
    )


@app.route("/<int:editionN>/<int:modelN>")
# Display page for individual models in an edition
def model_page(editionN, modelN):
    pass


@app.route("/<int:editionN>/about")
# Display about page for specific edition
def editionAbout(editionN):
    aboutDir = f"{editionDir}/{editionN}"
    aboutFile = "about.md"
    aboutHtml = render_md(aboutDir, aboutFile)
    return render_template("editionTexts.html", text=aboutHtml)


@app.route("/<int:editionN>/project_background")
# Display about page for specific edition
def editionBackground(editionN):
    pass

if __name__ == "__main__":
    app.run()
