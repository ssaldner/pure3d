import os

from helpers.generic import readYaml
from helpers.files import dirExists
from settings import YAML_DIR, PROJECT_DIR


class Projects:
    def __init__(self, Messages):
        self.Messages = Messages
        self.projectStatus = readYaml(f"{YAML_DIR}/projectstatus.yaml")

    def addAuth(self, Auth):
        self.Auth = Auth

    def getProjectList(self):
        # to get enumeration of top level directories
        # these are joined with the "project" directory path to get
        # path of each project
        AUTH = self.Auth
        M = self.Messages
        numbers = []

        if not dirExists(PROJECT_DIR):
            M.error(f"Project directory {PROJECT_DIR} does not exist")
            return numbers

        with os.scandir(PROJECT_DIR) as ed:
            for entry in ed:
                if entry.is_dir():
                    name = entry.name
                    if name.isdigit():
                        projectId = int(name)
                        permitted = AUTH.authorise(projectId, "read")
                        if permitted:
                            numbers.append(int(name))
        return sorted(numbers)

    def getEditionsList(self, projectId):
        # to get enumeration of sub-directories under folder "editions"
        AUTH = self.Auth
        M = self.Messages

        permitted = AUTH.authorise(projectId, "read")
        if not permitted:
            return []

        editionIds = []
        editionDir = f"{PROJECT_DIR}/{projectId}/editions"

        if not dirExists(editionDir):
            M.error(f"Project directory {PROJECT_DIR} does not exist")
            return editionIds

        with os.scandir(editionDir) as md:
            for edition in md:
                if edition.is_dir():
                    name = edition.name
                    if name.isdigit():
                        editionIds.append(int(name))
        return sorted(editionIds)
