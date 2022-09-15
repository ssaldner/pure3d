import os


def readFile(fileDir, fileName):
    filePath = f"{fileDir}/{fileName}"
    if not os.path.isfile(filePath):
        return f"No file {fileName} in {fileDir}"
    return open(filePath)


def dirExists(path):
    return os.path.isdir(path)
