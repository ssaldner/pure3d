import os
import json
from textwrap import dedent
from markdown import markdown

from helpers.files import readYaml, readPath, listFiles
from helpers.generic import AttrDict
from helpers.messages import debug
from settings import YAML_DIR, DATA_DIR, DATA_URL

COMPONENT = dict(
    home=("texts/intro", "md", True),
    title=("meta/dc", "json", "dc.title"),
    icon=("candy/icon", "png", None),
    about=("texts/about", "md", True),
    intro=("texts/intro", "md", True),
    usage=("texts/usage", "md", True),
    description=("texts/description", "md", True),
)


class ProjectError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Projects:
    def __init__(self, Settings, Messages):
        self.Settings = Settings
        self.Messages = Messages
        self.projectStatus = readYaml(f"{YAML_DIR}/projectstatus.yaml")

    def addAuth(self, Auth):
        self.Auth = Auth

    def getLocation(
        self,
        item=None,
        projectId=None,
        projectItem=None,
        editionId=None,
        editionItem=None,
        extension=None,
    ):
        """Look up a resource.

        The resource will be returned as data url and as path in the file system.
        It will be checked if the resource exists.

        If anything is wrong, a `ProjectError` exception will be raised.

        Parameters
        ----------
        """

        location = ""
        if item:
            location += f"/{item}"
        if projectId:
            location += f"projects/{projectId}"
        if projectItem:
            location += f"/{projectItem}"
        if editionId:
            location += f"/editions/{editionId}"
        if editionItem:
            location += f"/{editionItem}"
        if extension:
            location += f".{extension}"

        path = f"{DATA_DIR}/{location}"
        url = f"{DATA_URL}/{location}"

        if extension is not None and not os.path.exists(path):
            debug(f"{path=}")
            raise ProjectError(f"location `{location}` not found")

        return (path, url)

    def getInfo(self, projectId, editionId, *components, data=True):
        componentData = AttrDict()

        try:
            for component in components:
                (item, extension, method) = COMPONENT[component]
                (path, url) = self.getLocation(
                    projectId=projectId,
                    editionId=editionId,
                    item=item,
                    extension=extension,
                )
                if data:
                    if extension == "json":
                        content = json.load(path)
                        if method:
                            content = data[method]
                    elif extension == "md":
                        content = readPath(path)
                        if method:
                            content = markdown(content)
                    else:
                        content = None
                else:
                    content = None

                componentData[component] = (path, url, content)

        except ProjectError as e:
            debug(f"{e=}")
            raise e

        return componentData

    def getScenes(self, projectId, editionId):
        try:
            (path, url) = self.getLocation(projectId=projectId, editionId=editionId)
        except ProjectError as e:
            raise e

        return listFiles(path, ".json")

    def wrapScenes(self, projectId, editionId, sceneNames):
        Settings = self.Settings
        previewWidth = Settings["previewWidth"]
        previewHeight = Settings["previewHeight"]
        scenes = []

        for sceneName in sceneNames:
            scenes.append(
                dedent(
                    f"""
                    <div class="model">
                        <iframe
                            width="{previewWidth}" height="{previewHeight}"
                            src="/voyager/{projectId}/{editionId}/{sceneName}.json"/>
                        </iframe>
                    </div>
                    """
                )
            )

        scenes = "\n".join(scenes)

    def getProjectList(self):
        AUTH = self.Auth
        projectList = []

        try:
            projectIds = []
            (projectPath, projectUrl) = self.getLocation(item="", extension="")

            with os.scandir(projectPath) as ed:
                for entry in ed:
                    if entry.is_dir():
                        name = entry.name
                        if name.isdigit():
                            projectId = int(name)
                            permitted = AUTH.authorise(projectId, "read")
                            if permitted:
                                projectIds.append(int(name))

            for projectId in sorted(projectIds):
                projectData = Projects.getInfo(projectId, None, "home", "title", "icon")
                url = projectData["home"][1]
                icon = projectData["icon"][1]
                title = projectData["title"][2]
                projectList.append(url, icon, title)

        except ProjectError:
            pass
        return projectList

    def getEditionsList(self, projectId):
        # to get enumeration of sub-directories under folder "editions"
        AUTH = self.Auth

        permitted = AUTH.authorise(projectId, "read")
        if not permitted:
            return []

        editionList = []

        try:
            (editionPath, editionUrl) = self.getLocation(
                projectId=projectId, item="editions", extension=""
            )

            editionIds = []

            with os.scandir(editionPath) as md:
                for edition in md:
                    if edition.is_dir():
                        name = edition.name
                        if name.isdigit():
                            editionIds.append(int(name))

            for editionId in sorted(editionIds):
                editionData = Projects.getInfo(
                    projectId, editionId, "home", "title", "icon"
                )
                url = editionData["home"][1]
                icon = editionData["icon"][1]
                title = editionData["title"][2]
                editionList.append(url, icon, title)

        except ProjectError:
            pass
        return editionList

    def wrapItemLinks(self, linkItems):
        wrapped = []

        for (url, icon, title) in linkItems:
            wrapped.append(
                f"""<a href="{url}"><img src="{icon}"><br>{title}</a><br>\n"""
            )

        return "\n".join(wrapped)
