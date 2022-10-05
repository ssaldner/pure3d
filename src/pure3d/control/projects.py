import os
import json
from textwrap import dedent
from markdown import markdown

from helpers.files import readYaml, readPath, listFiles
from helpers.generic import AttrDict


COMPONENT = dict(
    me=(None, None, None, None),
    home=("texts/intro", "md", True, ""),
    about=("texts/about", "md", True, "## About\n\n"),
    intro=("texts/intro", "md", True, ""),
    usage=("texts/usage", "md", True, "## Guide\n\n"),
    description=("texts/description", "md", True, "## Description\n\n"),
    sources=("texts/sources", "md", True, "## Sources\n\n"),
    title=("meta/dc", "json", "dc.title", None),
    icon=("candy/icon", "png", None, None),
    list=(None, None, None, None),
)

PROJECTS = "projects"
EDITIONS = "editions"


class ProjectError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Projects:
    def __init__(self, Config, Messages):
        self.Config = Config
        self.Messages = Messages

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
        missingOk=False,
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
            location += f"{sep}{PROJECTS}/{projectId}"
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
            location += f"{extension}"

        locationPath = location
        if sceneName:
            locationPath = f"{locationPath}.json"

        path = f"{dataDir}/{locationPath}"
        url = (
            (("" if location.startswith("/") else "/") + location)
            if api
            else f"/{dataUrl}/{location}"
        )

        exists = None

        if not api or sceneName:
            if os.path.exists(path):
                exists = True
            else:
                if missingOk:
                    exists = False
                else:
                    raise ProjectError(f"location `{location}` not found")

        return (path, url, exists)

    def getInfo(self, projectId, editionId, sceneName, *components, missingOk=False):
        componentData = AttrDict()

        try:
            for component in components:
                if component not in COMPONENT:
                    raise ProjectError(f"Unknown component {component}")

                (item, extension, method, before) = COMPONENT[component]
                if extension is not None:
                    extension = f".{extension}"

                (path, url, exists) = self.getLocation(
                    projectId,
                    editionId,
                    sceneName if item is None else None,
                    item,
                    extension,
                    api=item is None,
                    missingOk=missingOk,
                )
                if extension in {".json", ".md"}:
                    content = readPath(path)
                    if extension == ".json":
                        content = json.loads(content) if exists else {}
                        if method:
                            content = content.get(method, None)
                    elif extension == ".md":
                        if exists:
                            content = readPath(path)
                        else:
                            content = f"~~missing {component}~~\n\n"
                        if method:
                            content = markdown(before + content)
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
            (basePath, baseUrl, exists) = self.getLocation(
                projectId,
                editionId,
                None,
                PROJECTS
                if projectId is None
                else EDITIONS
                if editionId is None
                else None,
                None,
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
                    (projectSel, editionSel) = (
                        (theItem, None) if projectId is None else (projectId, theItem)
                    )
                    data = self.getInfo(
                        projectSel, editionSel, None, "me", "title", "icon"
                    )
                    url = data["me"][1]
                    icon = data["icon"][1]
                    title = data["title"][2]
                    kind = True
                else:
                    data = self.getInfo(projectId, editionId, theItem, "me")
                    url = data["me"][1]
                    icon = f"/voyager/{projectId}/{editionId}/{theItem}"
                    title = theItem
                    kind = False
                theList.append((kind, url, icon, title))

        except ProjectError:
            pass

        wrapped = self.wrapItemLinks(theList, sceneName)
        return wrapped

    def wrapItemLinks(self, linkItems, sceneName):
        wrapped = []

        for (i, (kind, url, icon, title)) in enumerate(linkItems):
            if kind:
                wrapped.append(
                    f"""<a href="{url}"><img class="previewicon" src="{icon}">"""
                    f"""<br>{title}</a><hr><br>\n"""
                )
            else:
                isActive = (sceneName is None and i == 0) or (
                    sceneName is not None and title == sceneName
                )
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
                        if isActive
                        else f"""<p><a href="{url}">{title}</a></p>\n"""
                    )
                )
                if False:
                    opened = "open" if isActive else ""
                    active = "active" if isActive else ""
                    wrapped.append(
                        dedent(
                            f"""
                            <details {opened}>
                                <summary>
                                    <a class="button {active}" href="{url}">{title}</a>
                                </summary>
                                <iframe
                                    class="previewer"
                                    src="{icon}"/>
                                </iframe>
                            </details>
                            """
                        )
                    )

        return "\n".join(wrapped)
