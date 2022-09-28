import os
import yaml


def readPath(filePath):
    if os.path.isfile(filePath):
        with open(filePath) as fh:
            text = fh.read()
        return text
    return ""


def readFile(fileDir, fileName):
    filePath = f"{fileDir}/{fileName}"
    if not os.path.isfile(filePath):
        return f"No file {fileName} in {fileDir}"
    return open(filePath)


def readYaml(path):
    with open(path) as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)
    return data


def dirExists(path):
    return os.path.isdir(path)


def listFiles(path, ext):
    if not os.path.isdir(path):
        return []

    files = []

    theExt = f".{ext}"
    nExt = len(theExt)
    with os.scandir(path) as dh:
        for entry in dh:
            name = entry.name
            if name.endswith(theExt) and entry.is_file():
                files.append(name[0:-nExt])

    return files
