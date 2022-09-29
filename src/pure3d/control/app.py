import os

from flask import Flask, render_template, abort, redirect, make_response

from helpers.messages import error, Messages
from settings import Settings
from projects import Projects, ProjectError
from users import Users

from authorise import Auth

Config = Settings().getConfig()

# create and configure app
app = Flask(__name__, static_folder="../static")

app.secret_key = Config.secret_key

M = Messages(app)
Users = Users(Config)
Projects = Projects(Config, M)
AUTH = Auth(M, Users, Projects)
Projects.addAuth(AUTH)


def redirectResult(url, good):
    code = 302 if good else 303
    return redirect(url, code=code)


# app url routes start here


@app.route("/")
@app.route("/home")
def home():
    try:
        projectData = Projects.getInfo(None, None, "home")
    except ProjectError as e:
        M.error(e)
        abort(404)

    error(f"{projectData=}")

    return render_template(
        "index.html",
        text=projectData.home[2],
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/about")
def about():
    M = Messages(app)

    try:
        projectData = Projects.getInfo(None, None, "about")
    except ProjectError as e:
        M.error(e)
        abort(404)

    return render_template(
        "about.html",
        text=projectData.about[2],
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/supriseme")
def supriseme():
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


@app.route("/projects")
def projects():
    M = Messages(app)

    try:
        (homePath, homeUrl, homeContent) = Projects.getInfo(None, None, "home")["home"]
        projectList = Projects.getProjectList()

    except ProjectError as e:
        M.error(e)
        abort(404)

    projectLinks = Projects.wrapItemLinks(projectList)

    return render_template(
        "projectList.html",
        url=homeUrl,
        projectLinks=projectLinks,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/<int:projectId>")
def projectPage(projectId):
    M = Messages(app)

    try:
        (homePath, homeUrl, homeContent) = Projects.getInfo(None, None, "home")["home"]
        projectData = Projects.getInfo(
            projectId,
            None,
            "home",
            "title",
            "icon",
            "about",
            "intro",
            "usage",
            "description",
        )

        editionList = Projects.getEditionsList(projectId)

    except ProjectError as e:
        M.error(e)
        abort(404)

    editionLinks = Projects.wrapItemLinks(editionList)

    return render_template(
        "project.html",
        url=homeUrl,
        projectData=projectData,
        editionLinks=editionLinks,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/<int:projectId>/about")
def projectAbout(projectId):
    M = Messages(app)

    try:
        (homePath, homeUrl, homeContent) = Projects.getInfo(None, None, "home")["home"]
        projectData = Projects.getInfo(
            projectId, None, "home", "title", "icon", "about"
        )

    except ProjectError as e:
        M.error(e)
        abort(404)

    return render_template(
        "projectTexts.html",
        url=homeUrl,
        projectData=projectData,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/<int:projectId>/description")
def projectDescription(projectId):
    M = Messages(app)

    try:
        (homePath, homeUrl, homeContent) = Projects.getInfo(None, None, "home")["home"]
        projectData = Projects.getInfo(
            projectId, None, "home", "title", "icon", "description"
        )

    except ProjectError as e:
        M.error(e)
        abort(404)

    return render_template(
        "projectTexts.html",
        url=homeUrl,
        projectData=projectData,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/<int:projectId>/editions/<int:editionId>")
def editionPage(projectId, editionId):
    M = Messages(app)

    try:
        (homePath, homeUrl, homeContent) = Projects.getInfo(None, None, "home")["home"]
        projectData = Projects.getInfo(
            projectId,
            None,
            "home",
            "title",
            "icon",
            "intro",
        )
        editionData = Projects.getInfo(
            projectId,
            editionId,
            "home",
            "title",
            "icon",
            "about",
        )
        sceneNames = Projects.getScenes(projectId, editionId)
        scenes = Projects.wrapScenes(projectId, editionId, sceneNames)

    except ProjectError as e:
        M.error(e)
        abort(404)

    return render_template(
        "edition.html",
        url=homeUrl,
        projectData=projectData,
        editionData=editionData,
        scenes=scenes,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/voyager/<int:projectId>/<int:EditionId>/<string:scene>")
def voyager(projectId, editionId, scene):
    extDev = "min"

    (editionItem, extension) = scene.rsplit(".", 1)

    try:
        (rootUrl, rootPath) = Projects.getLocation(
            projectId=projectId,
            editionId=editionId,
            editionItem=editionItem,
            extension=extension,
        )
    except ProjectError as e:
        M.error(e)
        abort(404)

    return render_template(
        "voyager.html",
        ext=extDev,
        root=rootUrl,
        scene=scene,
        messages=M.generateMessages(),
        testUsers=AUTH.wrapTestUsers(),
    )


@app.route("/data/<path:path>")
def data(path):
    dataDir = Config.dataDir

    dataPath = f"{dataDir}/{path}"
    if not os.path.isfile(dataPath):
        error(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)


if __name__ == "__main__":
    app.run()
