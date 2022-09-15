from helpers.generic import readYaml
from settings import YAML_DIR


def getProjectStatus():
    projectStatus = readYaml(f"{YAML_DIR}/projectstatus.yaml")
    return projectStatus
