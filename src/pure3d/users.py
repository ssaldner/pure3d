from helpers.generic import readYaml
from settings import YAML_DIR


def getTestUsers():
    testUsers = readYaml(f"{YAML_DIR}/testusers.yaml")
    return testUsers


def getPermissions():
    authData = readYaml(f"{YAML_DIR}/authorise.yaml")
    return authData


def getUserProject():
    projectUsers = readYaml(f"{YAML_DIR}/projectusers.yaml")

    userProjects = {}
    for (project, users) in projectUsers.items():
        for (user, role) in users.items():
            userProjects.setdefault(user, {})[project] = role
    return dict(projectUsers=projectUsers, userProjects=userProjects)
