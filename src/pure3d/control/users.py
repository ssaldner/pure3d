from helpers.generic import readYaml
from helpers.messages import debug
from settings import YAML_DIR


def getTestUsers():
    testUsers = readYaml(f"{YAML_DIR}/testusers.yaml")
    userNameById = {}
    userRoleById = {}
    testUserIds = set()

    for (name, info) in testUsers.items():
        userId = info["id"]
        if userId in testUserIds:
            prevName = userNameById[userId]
            debug(f"WARNING: duplicate test user {userId} = {name}, {prevName}")
            continue
        testUserIds.add(userId)
        userNameById[userId] = name
        userRoleById[userId] = info["role"]

    return dict(
        testUserIds=testUserIds, userNameById=userNameById, userRoleById=userRoleById
    )


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
