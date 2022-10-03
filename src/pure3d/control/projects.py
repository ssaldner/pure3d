import os
import json
from textwrap import dedent
from markdown import markdown

from helpers.files import readYaml, readPath, listFiles
from helpers.generic import AttrDict


COMPONENT = dict(
    me=(None, None, None),
    home=("texts/intro", "md", True),
    about=("texts/about", "md", True),
    intro=("texts/intro", "md", True),
    usage=("texts/usage", "md", True),
    description=("texts/description", "md", True),
    title=("meta/dc", "json", "dc.title"),
    icon=("candy/icon", "png", None),
    list=(None, None, None),
)


class ProjectError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Projects:
    def __init__(self, Config, Messages):
        self.Config = Config
        self.Messages = Messages
        self.comps = tuple(COMPONENT)

        yamlDir = Config.yamlDir
        self.projectStatus = readYaml(f"{yamlDir}/projectstatus.yaml")

    def addAuth(self, Auth):
        self.Auth = Auth

    def getLocation(
        self,
        item,
        projectId,
        projectItem,
        editionId,
        editionItem,
        extension,
        api=False,
    ):
        """Look up the location of a resource.

        The resource will be returned as data url and as path in the file system.
        It will be checked if the resource exists.

        If anything is wrong, a `ProjectError` exception will be raised.

        Parameters
        ----------
        """

        Config = self.Config
        dataDir = Config.dataDir
        dataUrl = Config.dataUrl

        location = ""
        if item:
            sep = "/" if location else ""
            location += f"{sep}{item}"
        if projectId:
            sep = "/" if location else ""
            location += f"{sep}{projectId}"
        if projectItem:
            sep = "/" if location else ""
            location += f"{sep}{projectItem}"
        if editionId:
            sep = "/" if location else ""
            location += f"{sep}{editionId}"
        if editionItem:
            sep = "/" if location else ""
            location += f"{sep}{editionItem}"
        if extension:
            location += f".{extension}"

        path = f"{dataDir}/{location}"
        url = location if api else f"/{dataUrl}/{location}"
        print(f"{url=}")

        if not api and extension is not None and not os.path.exists(path):
            raise ProjectError(f"location `{location}` not found")

        return (path, url)

    def getInfo(self, projectId, editionId, *components):
        componentData = AttrDict()

        try:
            for component in components:
                if component not in COMPONENT:
                    raise ProjectError(f"Unknown component {component}")

                (it, extension, method) = COMPONENT[component]
                item = None
                projectItem = None
                editionItem = None

                if projectId is None:
                    item = it
                else:
                    item = "projects"
                    if editionId is None:
                        projectItem = it
                    else:
                        projectItem = "editions"
                        editionItem = it

                (path, url) = self.getLocation(
                    item,
                    projectId,
                    projectItem,
                    editionId,
                    editionItem,
                    extension,
                    api=it is None,
                )
                if extension in {"json", "md"}:
                    content = readPath(path)
                    if extension == "json":
                        content = json.loads(content)
                        if method:
                            content = content[method]
                    elif extension == "md":
                        content = readPath(path)
                        if method:
                            content = markdown(content)
                elif component == "list":
                    print(f"getList {projectId=}")
                    content = self.getList(projectId)
                    print(f"{content=}")
                else:
                    content = None

                componentData[component] = (path, url, content)

        except ProjectError as e:
            raise e

        return componentData

    def getScenes(self, projectId, editionId):
        try:
            (path, url) = self.getLocation("projects", projectId, "editions", editionId, None, None)
        except ProjectError as e:
            raise e

        return listFiles(path, ".json")

    def wrapScenes(self, projectId, editionId, sceneNames):
        scenes = []

        for sceneName in sceneNames:
            scenes.append(
                dedent(
                    f"""
                    <div class="model">
                        <iframe
                            class="previewer"
                            src="/voyager/{projectId}/{editionId}/{sceneName}.json"/>
                        </iframe>
                    </div>
                    """
                )
            )

        scenes = "\n".join(scenes)

    def getList(self, projectId):
        print("in getList")
        AUTH = self.Auth
        theList = []

        theIds = []
        (basePath, baseUrl) = self.getLocation(
            "projects",
            projectId,
            None if projectId is None else "editions",
            None,
            None,
            "",
            api=True,
        )
        print(f"{basePath=} {baseUrl=}")

        try:
            with os.scandir(basePath) as ed:
                for entry in ed:
                    if entry.is_dir():
                        name = entry.name
                        if name.isdigit():
                            theId = int(name)
                            args = (
                                (theId, None)
                                if projectId is None
                                else (projectId, theId)
                            )
                            permitted = AUTH.authorise(*args, "read")
                            if permitted:
                                theIds.append(int(name))

            print(f"{theIds=}")
            for theId in sorted(theIds):
                args = (theId, None) if projectId is None else (projectId, theId)
                data = self.getInfo(*args, "me", "title", "icon")
                url = data["me"][1]
                icon = data["icon"][1]
                title = data["title"][2]
                theList.append((url, icon, title))

        except ProjectError:
            pass

        wrapped = self.wrapItemLinks(theList)
        return wrapped

    def wrapItemLinks(self, linkItems):
        wrapped = []

        for (url, icon, title) in linkItems:
            wrapped.append(
                f"""<a href="{url}"><img class="previewicon" src="{icon}">"""
                f"""<br>{title}</a><br>\n"""
            )

        return "\n".join(wrapped)
