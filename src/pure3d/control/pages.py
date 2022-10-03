from textwrap import dedent
from flask import abort, render_template

TABS = (
    ("home", "Home"),
    ("about", "About"),
    ("projects", "3D Projects"),
    ("directory", "3D Directory"),
    ("surpriseme", "Surprise Me"),
    ("advancedsearch", "Advanced Search"),
)


class Pages:
    def __init__(self, Messages, Projects, ProjectError, Auth):
        self.Messages = Messages
        self.Projects = Projects
        self.ProjectError = ProjectError
        self.Auth = Auth

    def base(
        self, url, projectId, editionId, *comps, title=None, content=None
    ):
        M = self.Messages
        Projects = self.Projects
        ProjectError = self.ProjectError
        Auth = self.Auth

        try:
            projectData = Projects.getInfo(projectId, editionId, *comps)
        except ProjectError as e:
            M.error(e)
            abort(404)

        navigation = self.navigation(url)
        material = []

        for comp in comps:
            material.append(
                dedent(
                    f"""
            <div id="{comp}">
                {projectData[comp][2]}
            </div>
            """
                )
            )

        material = "\n".join(material)

        title = title or ""
        content = content or ""

        return render_template(
            "index.html",
            navigation=navigation,
            material=title + material + content,
            messages=M.generateMessages(),
            testUsers=Auth.wrapTestUsers(),
        )

    def navigation(self, url):
        search = dedent(
            """
            <span class="search-bar">
                <input
                    type="search"
                    name="search"
                    placeholder="search item"
                >
                <input type="submit" value="Search">
            </span>
            """
        )
        html = ["""<div class="tabs">"""]

        for (tab, label) in TABS:
            active = "active" if url == tab else ""
            html.append(
                dedent(
                    f"""
                    <a
                        href="/{tab}"
                        class="button large {active}"
                    >{label}</a>
                """
                )
            )
        html.append(search)
        html.append("</div>")
        return "\n".join(html)
