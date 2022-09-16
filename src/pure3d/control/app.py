from flask import Flask, render_template, url_for, abort, redirect, make_response
import sys
import os
from markdown import markdown

from helpers.generic import renderMd
from helpers.messages import debug, Messages
from helpers.files import readFile
from settings import BASE, DATA_DIR, PROJECT_DIR, SECRET_FILE
from dublincore import dcReaderJSON
from projects import Projects

from authorise import Auth

# create and configure app
app = Flask(__name__, static_folder="../static")

if not os.path.exists(SECRET_FILE):
    debug(f"Missing secret file for sessions: {SECRET_FILE}")
    debug("Create that file with contents a random string like this:")
    debug("fjOL901Mc3XZy8dcbBnOxNwZsOIBlul")
    debug("But do not choose this one.")
    debug("Use your password manager to create a random one.")
    debug("Aborting ...")
    sys.exit(1)

with open(SECRET_FILE) as fh:
    app.secret_key = fh.read()


title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D website"

# variables

WIDTH = "600px"
HEIGHT = "600px"

M = Messages(app)
Projects = Projects(M)
AUTH = Auth(M, Projects)
Projects.addAuth(AUTH)


def redirectResult(url, good):
    code = 302 if good else 303
    return redirect(url, code=code)


# app url routes start here


@app.route("/")
@app.route("/home")
# Display home page
def home():

    return render_template(
        "index.html",
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/about")
# Display the About page
def about():
    M = Messages(app)

    fileDir = f"{BASE}/src/dip"
    fileName = "about.md"
    fh = readFile(fileDir, fileName)
    if type(fh) is str:
        M.error(fh)
        text = ""
    else:
        text = fh.read()

    html = markdown(text)

    return render_template(
        "about.html",
        about=html,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/projects")
def projects():
    M = Messages(app)

    # display list of projects on home page
    # used "dc.title" from the Dublin Core metadata
    projectIds = Projects.getProjectList()

    projectData = {}

    for i in projectIds:
        jsonDir = f"{PROJECT_DIR}/{i}/meta"
        jsonField = "dc.title"
        title = dcReaderJSON(M, jsonDir, jsonField)

        url = f"""/{i}"""

        candy = f"projects/{i}/candy/icon.png"

        # display project logo as banner
        logo = url_for("data", path=candy)

        projectData[i] = dict(title=title, url=url, logo=logo)

    projectLinks = []  # to get url redirections of individual pages of each project

    for (i, data) in sorted(projectData.items()):
        title = data["title"]
        url = data["url"]
        logo = data["logo"]
        projectLinks.append(
            f"""
            <a href="{url}"><img src="{logo}"></a><br>
            <a href="{url}">{title}</a><br>
        """
        )

    projectLinks = "\n".join(projectLinks)

    return render_template(
        "projectList.html",
        url=url,
        title=title,
        projectLinks=projectLinks,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/supriseme")
def supriseme():
    # M = Messages(app)

    pass


@app.route("/login")
def login():
    if AUTH.authenticate(login=True):
        good = True
    else:
        good = False
    return redirectResult("/", good)


@app.route("/logout")
def logout():
    AUTH.deauthenticate()
    return redirectResult("/", True)


@app.route("/register")
def register():
    # M = Messages(app)

    pass


@app.route("/<int:projectId>/about")
# Display about page for specific project
def projectAbout(projectId):
    M = Messages(app)

    aboutDir = f"{PROJECT_DIR}/{projectId}"
    aboutFile = "about.md"
    aboutHtml = renderMd(M, aboutDir, aboutFile)

    homeUrl = url_for("project_page", projectId=projectId)
    bgUrl = url_for("projectBackground", projectId=projectId)

    return render_template(
        "projectTexts.html",
        text=aboutHtml,
        homeUrl=homeUrl,
        bgUrl=bgUrl,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/<int:projectId>/<int:editionId>")
# Display page for individual editions in an project
def edition_page(projectId, editionId):
    M = Messages(app)

    ed = f"{PROJECT_DIR}/{projectId}/editions/{editionId}"  # edition directory on filesystem
    root = f"data/projects/{projectId}/editions/{editionId}/"  # edition root url

    candyLogo = f"projects/{projectId}/candy/logo.png"

    # display project logo as banner
    logo = url_for("data", path=candyLogo)

    # render About information
    aboutFile = "about.md"
    aboutHtml = renderMd(M, ed, aboutFile)

    # urls for different tabs on the project page
    homeUrl = url_for("project_page", projectId=projectId)
    aboutUrl = url_for("projectAbout", projectId=projectId)
    bgUrl = url_for("projectBackground", projectId=projectId)

    # displaying 3d editions
    # accesses the scene file
    for file in os.listdir(ed):
        if file.endswith(".json"):
            scene = file

    return render_template(
        "edition.html",
        aboutHtml=aboutHtml,
        projectId=projectId,
        editionId=editionId,
        scene=scene,
        height=HEIGHT,
        width=WIDTH,
        homeUrl=homeUrl,
        aboutUrl=aboutUrl,
        bgUrl=bgUrl,
        root=root,
        logo=logo,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/voyager/<string:scene>/<path:root>")
def voyager(scene, root):
    # url for voyager in explorer mode
    M = Messages(app)
    ext = "min"
    root = f"/{root}"

    return render_template(
        "voyager.html",
        ext=ext,
        root=root,
        scene=scene,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
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


@app.route("/<int:projectId>")
# Display for projects page(s)
def project_page(projectId):
    M = Messages(app)

    pd = f"{PROJECT_DIR}/{projectId}"
    candyLogo = f"projects/{projectId}/candy/logo.png"

    # display title
    jsonDir = f"{PROJECT_DIR}/{projectId}/meta"
    jsonField = "dc.title"
    pd_title = dcReaderJSON(M, jsonDir, jsonField)

    # display project logo as banner
    logo = url_for("data", path=candyLogo)

    # rendering texts
    introFile = "intro.md"
    usageFile = "usage.md"

    introHtml = renderMd(M, pd, introFile)
    usageHtml = renderMd(M, pd, usageFile)

    # url variables for tabs on page
    aboutUrl = url_for("projectAbout", projectId=projectId)
    bgUrl = url_for("projectBackground", projectId=projectId)

    # hyper-linked editions list
    editionIds = Projects.getEditionsList(projectId)
    editionData = {}

    for j in editionIds:
        editionDir = f"{pd}/editions/{j}"
        editionFile = "title.txt"
        nameFile = os.path.join(editionDir, editionFile)
        with open(nameFile) as f:
            title = f.read()

        url = f"""/{projectId}/{j}"""
        candyIcon = f"projects/{projectId}/editions/{j}/candy/icon.png"
        icon = url_for("data", path=candyIcon)
        editionData[j] = dict(title=title, url=url, icon=icon)

    editionLinks = []

    for (i, data) in sorted(editionData.items()):
        title = data["title"]
        url = data["url"]
        icon = data["icon"]
        editionLinks.append(
            f"""
            <a href="{url}"><img src="{icon}" alt="edition icon"><br>
            <a href="{url}">{title}</a><br>
        """
        )

    editionLinks = "\n".join(editionLinks)

    return render_template(
        "project.html",
        usage=usageHtml,
        intro=introHtml,
        editioN=projectId,
        aboutUrl=aboutUrl,
        bgUrl=bgUrl,
        editionLinks=editionLinks,
        logo=logo,
        icon=icon,
        pd_title=pd_title,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/<int:projectId>/project_background")
# Display about page for specific project
def projectBackground(projectId):
    M = Messages(app)
    ed = f"{PROJECT_DIR}/{projectId}"
    backgroundFile = "description.md"
    backgroundHtml = renderMd(M, ed, backgroundFile)

    aboutUrl = url_for("projectAbout", projectId=projectId)
    homeUrl = url_for("project_page", projectId=projectId)

    return render_template(
        "projectTexts.html",
        text=backgroundHtml,
        homeUrl=homeUrl,
        aboutUrl=aboutUrl,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/<int:projectId>/sources")
# Display about page for specific project
def projectSources(projectId):
    # M = Messages(app)
    pass


if __name__ == "__main__":
    app.run()
