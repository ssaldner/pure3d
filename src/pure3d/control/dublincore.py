import json
from helpers.files import readFile


def dcReaderJSON(M, dcDir, dcField):
    # to read different values from the Dublin core file
    dcFile = "dc.json"
    fh = readFile(dcDir, dcFile)
    if type(fh) is str:
        M.error(fh)
        dcJson = {}
    else:
        dcJson = json.load(fh)

    if dcField in dcJson:
        dcFieldValue = dcJson[dcField]
    else:
        M.warning("No '{dcFieldValue}' in Dublin Core metadata")
        dcFieldValue = "Requested information not avilable"
    return dcFieldValue
