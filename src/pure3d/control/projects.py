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
    def __init__(self, Config, Viewers, Messages):
        self.Config = Config
        self.Viewers = Viewers
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

    def getInfo(
        self,
        projectId,
        editionId,
        sceneName,
        viewerVersion,
        *components,
        missingOk=False,
    ):
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
                    content = self.getList(
                        projectId, editionId, sceneName, viewerVersion
                    )
                else:
                    content = None

                componentData[component] = (path, url, content)

        except ProjectError as e:
            raise e

        return componentData

    def getList(self, projectId, editionId, sceneName, viewerVersion):
        """Get a list of items.

        If projectId is None: projects
        Else, if editionId is None: editions,
        Else: scene names for that edition
        """
        return (
            self.getProjects()
            if projectId is None
            else self.getEditions(projectId)
            if editionId is None
            else self.getScenes(projectId, editionId, sceneName, viewerVersion)
        )

    def getProjects(self):
        AUTH = self.Auth
        wrapped = []

        try:
            (basePath, baseUrl, exists) = self.getLocation(
                None,
                None,
                None,
                PROJECTS,
                None,
                api=True,
            )
            theItems = []
            with os.scandir(basePath) as ed:
                for entry in ed:
                    if entry.is_dir():
                        name = entry.name
                        if name.isdigit():
                            theId = int(name)
                            permitted = AUTH.authorise(theId, None, "read")
                            if permitted:
                                theItems.append(int(name))

            for theItem in sorted(theItems):
                projectSel = theItem
                data = self.getInfo(projectSel, None, None, None, "me", "title", "icon")
                url = data["me"][1]
                icon = data["icon"][1]
                title = data["title"][2]
                wrapped.append(
                    f"""<a href="{url}"><img class="previewicon" src="{icon}">"""
                    f"""<br>{title}</a><hr><br>\n"""
                )

        except ProjectError:
            pass

        return "\n".join(wrapped)

    def getEditions(self, projectId):
        AUTH = self.Auth
        wrapped = []

        try:
            (basePath, baseUrl, exists) = self.getLocation(
                projectId,
                None,
                None,
                EDITIONS,
                None,
                api=True,
            )
            theItems = []
            with os.scandir(basePath) as ed:
                for entry in ed:
                    if entry.is_dir():
                        name = entry.name
                        if name.isdigit():
                            theId = int(name)
                            permitted = AUTH.authorise(projectId, theId, "read")
                            if permitted:
                                theItems.append(int(name))

            for theItem in sorted(theItems):
                data = self.getInfo(
                    projectId, theItem, None, None, "me", "title", "icon"
                )
                url = data["me"][1]
                icon = data["icon"][1]
                title = data["title"][2]
                wrapped.append(
                    f"""<a href="{url}"><img class="previewicon" src="{icon}">"""
                    f"""<br>{title}</a><hr><br>\n"""
                )

        except ProjectError:
            pass

        return "\n".join(wrapped)

    def getScenes(self, projectId, editionId, sceneName, viewerVersion):
        AUTH = self.Auth
        Viewers = self.Viewers
        wrapped = []

        permitted = AUTH.authorise(projectId, editionId, "read")
        if not permitted:
            return []

        if viewerVersion is None:
            viewerVersion = Viewers.prefixes[-1]
        (viewer, version) = viewerVersion.split("-", 1)

        try:
            (basePath, baseUrl, exists) = self.getLocation(
                projectId,
                editionId,
                None,
                None,
                None,
                api=True,
            )
            theItems = listFiles(basePath, ".json")

            for (i, theItem) in enumerate(sorted(theItems)):
                data = self.getInfo(
                    projectId, editionId, theItem, None, "me"
                )
                url = data["me"][1]
                specifier = f"{projectId}/{editionId}/{theItem}"
                title = theItem
                isActive = (sceneName is None and i == 0) or (
                    sceneName is not None and title == sceneName
                )

                buttonRow = []
                frame = ""

                for vv in Viewers.prefixes:
                    vActive = "active" if isActive and vv == viewerVersion else ""
                    elem = "a"
                    attStr = ""

                    if vActive:
                        frame = dedent(
                            f"""
                            <div class="model">
                                <iframe
                                    class="previewer"
                                    src="/viewer/{viewerVersion}/{specifier}"/>
                                </iframe>
                                <span class="active">{title}</span>
                            </div>
                            """
                        )
                        elem = "span"
                    else:
                        attStr = f""" href="{url}/{vv}" """

                    buttonRow.append(
                        f"""
                        <{elem}
                            class="button {vActive}"
                            {attStr}
                        >{vv}</{elem}>
                        """
                    )

                buttonRow = "\n".join(buttonRow)
                caption = f"""<p>{title} {buttonRow}</p>\n"""
                wrapped.append(f"""{frame} {caption}""")

        except ProjectError:
            pass

        return "\n".join(wrapped)

    def wrapItemLinks(self, linkItems, sceneName, viewerVersion):
        Viewers = self.Viewers
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
                if isActive:
                    buttonRow = []

                    for vv in Viewers.prefixes:
                        vActive = ""
                        if vv == viewerVersion:
                            (viewer, version) = viewerVersion.split("-", 1)
                            wrapped.append(
                                dedent(
                                    f"""
                                    <div class="model">
                                        <iframe
                                            class="previewer"
                                            src="/viewer/{viewerVersion}/{icon}"/>
                                        </iframe>
                                        <span class="active">{title}</span>
                                    </div>
                                    """
                                )
                            )
                            vActive = "active"

                        buttonRow.append(
                            f"""
                            <a
                                class="button {vActive}"
                                href="{url}/{vv}"
                            >{viewerVersion}</a>
                            """
                        )
                    wrapped.append("\n".join(buttonRow))
                else:
                    wrapped.append(f"""<p>{title}<a href="{url}"></a></p>\n""")

        return "\n".join(wrapped)
