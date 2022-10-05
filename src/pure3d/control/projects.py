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
        projectId,
        editionId,
        sceneName,
        item,
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
        if projectId:
            sep = "/" if location else ""
            location += f"{sep}projects/{projectId}"
        if editionId:
            sep = "/" if location else ""
            location += f"{sep}editions/{editionId}"
        if sceneName:
            sep = "/" if location else ""
            location += f"{sep}{sceneName}"
        if item:
            sep = "/" if location else ""
            location += f"{sep}{item}"
        if extension:
            location += f".{extension}"

        locationPath = location
        if sceneName:
            locationPath = f"{locationPath}.{json}"

        path = f"{dataDir}/{locationPath}"
        url = location if api else f"/{dataUrl}/{location}"
        print(f"{dataDir=} {dataUrl=} {sceneName=} {item=} {path=} {url=}")

        if (not api or sceneName) and not os.path.exists(path):
            raise ProjectError(f"location `{location}` not found")

        return (path, url)

    def getInfo(self, projectId, editionId, sceneName, *components):
        componentData = AttrDict()

        try:
            for component in components:
                print(f"{projectId=} {editionId=} {sceneName=} {component=}")
                if component not in COMPONENT:
                    raise ProjectError(f"Unknown component {component}")

                (item, extension, method) = COMPONENT[component]
                print(f"{item=} {extension=} {method=}")

                (path, url) = self.getLocation(
                    projectId,
                    editionId,
                    sceneName,
                    item,
                    extension,
                    api=item is None,
                )
                print(f"AAA {path=} {url=}")
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
                    content = self.getList(projectId, editionId, sceneName)
                else:
                    content = None

                componentData[component] = (path, url, content)

        except ProjectError as e:
            raise e

        return componentData

    def getList(self, projectId, editionId, sceneName):
        """Get a list of items.

        If projectId is None: projects
        Else, if editionId is None: editions,
        Else: scene names for that edition
        """
        AUTH = self.Auth
        theList = []

        try:
            (basePath, baseUrl) = self.getLocation(
                projectId,
                editionId,
                sceneName,
                None,
                "",
                api=True,
            )
            if editionId is None:
                theItems = []
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
                                    theItems.append(int(name))
            else:
                theItems = listFiles(basePath, ".json")

            for theItem in sorted(theItems):
                if editionId is None:
                    args = (
                        (theItem, None) if projectId is None else (projectId, theItem)
                    )
                    data = self.getInfo(*args, sceneName, "me", "title", "icon")
                    url = data["me"][1]
                    icon = data["icon"][1]
                    title = data["title"][2]
                    kind = True
                else:
                    data = self.getInfo(projectId, editionId, sceneName, theItem, "me")
                    url = data["me"][1]
                    icon = f"/voyager/{projectId}/{editionId}/{theItem}.json"
                    title = theItem
                    kind = False
                theList.append((kind, url, icon, title))

        except ProjectError:
            pass

        wrapped = self.wrapItemLinks(theList)
        return wrapped

    def wrapItemLinks(self, linkItems, active=None):
        wrapped = []

        for (i, (kind, url, icon, title)) in enumerate(linkItems):
            if kind:
                wrapped.append(
                    f"""<a href="{url}"><img class="previewicon" src="{icon}">"""
                    f"""<br>{title}</a><br>\n"""
                )
            else:
                wrapped.append(
                    dedent(
                        f"""
                        <div class="model">
                            <iframe
                                class="previewer"
                                src="{icon}"/>
                            </iframe>
                            <span class="active">{title}</span>
                        </div>
                        """
                        if (active is None and i == 0)
                        or (active is not None and title == active)
                        else f"""<a href="{url}">{title}</a><br>\n"""
                    )
                )

        return "\n".join(wrapped)
