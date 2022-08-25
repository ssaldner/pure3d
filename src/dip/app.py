from flask import Flask, render_template
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


# functions


def editionsList():  # to get enumeration of top level directories
    numbers = []
    with os.scandir(editionDir) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


def render_md(mdPath, mdFile):  # to render markdown files
    filename = f"{mdPath}/texts/{mdFile}"
    with open(filename, "r") as f:
        text = f.read()
        html = markdown(text)
        return html


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
    return render_template("about.html")


@app.route("/<int:editionN>")
# Display for editions page(s)
def edition_page(editionN):
    print(f"I am here {editionN=}")
    introDir = f"{editionDir}/{editionN}"
    introFile = "intro.md"
    introHtml = render_md(introDir, introFile)
    return render_template("edition.html", intro=introHtml, editionN=editionN)


@app.route("/<int:editionN>/about")
# Display about page for specific edition
def editionAbout(editionN):
    pass


if __name__ == "__main__":
    app.run()
