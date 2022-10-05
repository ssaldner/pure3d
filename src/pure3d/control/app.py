import os

from flask import Flask, render_template, abort, redirect, make_response

from helpers.messages import error, Messages
from settings import Settings
from projects import Projects, ProjectError
from users import Users
from pages import Pages

from authorise import Auth

Config = Settings().getConfig()

# create and configure app
app = Flask(__name__, static_folder="../static")

app.secret_key = Config.secret_key

M = Messages(app)
Users = Users(Config)
Projects = Projects(Config, M)
Auth = Auth(M, Users, Projects)
Projects.addAuth(Auth)
Pages = Pages(M, Projects, ProjectError, Auth)


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
        left=(
            "home",
            "title",
            "icon",
            "intro",
            "about",
            "list",
        ),
        right=(
            "usage",
            "description",
        ),
    )


@app.route("/projects/<int:projectId>/editions/<int:editionId>")
def editionPage(projectId, editionId):
    return Pages.base(
        "projects",
        projectId=projectId,
        editionId=editionId,
        left=(
            "home",
            "title",
            "icon",
            "intro",
            "about",
            "list",
        ),
        right=(
            "usage",
            "description",
        ),
    )


@app.route("/projects/<int:projectId>/editions/<int:editionId>/<string:sceneName>")
def scenePage(projectId, editionId, sceneName):
    return Pages.base(
        "projects",
        projectId=projectId,
        editionId=editionId,
        sceneName=sceneName,
        left=(
            "home",
            "title",
            "icon",
            "intro",
            "about",
            "list",
        ),
        right=(
            "usage",
            "description",
        ),
    )


@app.route("/voyager/<int:projectId>/<int:EditionId>/<string:scene>")
def voyager(projectId, editionId, sceneName):
    extDev = "min"

    try:
        (rootUrl, rootPath) = Projects.getLocation(
            projectId,
            editionId,
            None,
            None,
            None,
        )
        Projects.getLocation(
            projectId,
            editionId,
            sceneName,
            None,
            None,
        )
    except ProjectError as e:
        M.error(e)
        abort(404)

    return render_template(
        "voyager.html",
        ext=extDev,
        root=rootUrl,
        scene=f"{sceneName}.json",
        messages=M.generateMessages(),
        testUsers=Auth.wrapTestUsers(),
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
