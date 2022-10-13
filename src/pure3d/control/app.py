import os

from flask import Flask, render_template, abort, redirect, make_response

from helpers.messages import error, Messages
from settings import Settings
from viewers import Viewers
from projects import Projects, ProjectError
from users import Users
from pages import Pages

from authorise import Auth

Config = Settings().getConfig()
Viewers = Viewers(Config)

# create and configure app
app = Flask(__name__, static_folder="../static")

app.secret_key = Config.secret_key

M = Messages(app)
Users = Users(Config)
Projects = Projects(Config, Viewers, M)
Auth = Auth(M, Users, Projects)
Projects.addAuth(Auth)
Pages = Pages(Config, M, Projects, ProjectError, Auth)


def redirectResult(url, good):
    code = 302 if good else 303
    return redirect(url, code=code)


# app url routes start here


@app.route("/")
@app.route("/home")
def home():
    return Pages.base("home", left=("home",))


@app.route("/about")
def about():
    return Pages.base("about", left=("home",), right=("about",))


@app.route("/surpriseme")
def surpriseme():
    content = "<h2>You will be surprised!</h2>"
    return Pages.base("surpriseme", left=("home",), content=content)


@app.route("/login")
def login():
    if Auth.authenticate(login=True):
        good = True
    else:
        good = False
    return redirectResult("/", good)


@app.route("/logout")
def logout():
    Auth.deauthenticate()
    return redirectResult("/", True)


@app.route("/projects")
def projects():
    title = """<h2>Scholarly projects</h2>"""

    return Pages.base("projects", left=("list",), title=title)


@app.route("/projects/<int:projectId>")
def projectPage(projectId):
    return Pages.base(
        "projects",
        projectId=projectId,
        left=("list",),
        right=(
            "title",
            "home",
            "about",
            "description",
        ),
    )


@app.route("/projects/<int:projectId>/editions/<int:editionId>")
def editionPage(projectId, editionId):
    return Pages.base(
        "projects",
        projectId=projectId,
        editionId=editionId,
        left=("list",),
        right=(
            "about",
            "sources",
        ),
    )


@app.route("/projects/<int:projectId>/editions/<int:editionId>/<string:sceneName>")
def scenePage(projectId, editionId, sceneName):
    return Pages.base(
        "projects",
        projectId=projectId,
        editionId=editionId,
        sceneName=sceneName,
        left=("list",),
        right=(
            "about",
            "sources",
        ),
    )


@app.route(
    "/projects/<int:projectId>/editions/<int:editionId>/<string:sceneName>/<string:viewerVersion>"
)
def sceneViewer(projectId, editionId, sceneName, viewerVersion):
    return Pages.base(
        "projects",
        projectId=projectId,
        editionId=editionId,
        sceneName=sceneName,
        viewerVersion=viewerVersion,
        left=("list",),
        right=(
            "about",
            "sources",
        ),
    )


@app.route(
    "/viewer/<string:viewerVersion>/<int:projectId>/<int:editionId>/<string:sceneName>"
)
def voyager(viewerVersion, projectId, editionId, sceneName):
    extDev = ".min"

    try:
        (rootPath, rootUrl, rootExists) = Projects.getLocation(
            projectId,
            editionId,
            None,
            None,
            None,
        )
        (scenePath, sceneUrl, sceneExists) = Projects.getLocation(
            projectId,
            editionId,
            sceneName,
            None,
            None,
        )
    except ProjectError as e:
        M.error(e)
        abort(404)

    viewerCode = Viewers.genHtml(
        viewerVersion, extDev, f"{rootUrl}/", f"{sceneName}.json"
    )

    return render_template(
        "voyager.html",
        viewerCode=viewerCode,
        ext=extDev,
        root=rootUrl + "/",
        scene=f"{sceneName}.json",
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
