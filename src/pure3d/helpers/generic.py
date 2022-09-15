import yaml
from markdown import markdown

from helpers.files import readFile


def render_md(M, mdPath, mdFile):
    # to render markdown files
    fileDir = f"{mdPath}/texts"
    fh = readFile(fileDir, mdFile)
    if type(fh) is str:
        M.addMessage("error", fh)
        html = ""
    else:
        text = fh.read()
        html = markdown(text)
    return html


def htmlEsc(val):
    """Escape certain HTML characters by HTML entities.

    To prevent them to be interpreted as HTML
    in cases where you need them literally.
    """

    return (
        ""
        if val is None
        else (
            str(val)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
        )
    )


def readYaml(path):
    with open(path) as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)
    return data
