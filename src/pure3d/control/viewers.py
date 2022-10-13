import os
from textwrap import dedent


class Viewers:
    def __init__(self, Config):
        self.Config = Config

        staticDir = Config.staticDir

        viewers = {
            v: []
            for (v, enabled) in Config.viewers.items()
            if enabled and os.path.isdir(f"{staticDir}/{v}")
        }
        self.viewers = viewers

        for v in viewers:
            viewerDir = f"{staticDir}/{v}"
            with os.scandir(viewerDir) as vh:
                for entry in vh:
                    if entry.is_dir():
                        viewers[v].append(entry.name)

        self.makeLinkPrefixes()

    def makeLinkPrefixes(self):
        viewers = self.viewers

        prefixes = []
        for (viewer, versions) in sorted(viewers.items()):
            for version in sorted(versions):
                prefixes.append(f"{viewer}-{version}")

        self.prefixes = prefixes

    def genHtml(self, viewerVersion, ext, root, scene):
        (viewer, version) = viewerVersion.split("-", 1)

        if viewer == "voyager":
            return dedent(
                f"""
                <head>
                <link href="/static/dist/fonts/fonts.css" rel="stylesheet"/>
                <link
                  rel="shortcut icon"
                  type="image/png"
                  href="/static/dist/favicon.png"
                />
                <link
                  rel="stylesheet"
                  href="/static/{viewer}/{version}/css/voyager-explorer{ext}.css"
                />
                <script
                  defer
                  src="/static/{viewer}/{version}/js/voyager-explorer{ext}.js">
                </script>
                </head>
                <body>
                <voyager-explorer
                  root="{root}"
                  document="{scene}"
                  resourceroot="/static/{viewer}/{version}"
                > </voyager-explorer>
                </body>
                """
            )
