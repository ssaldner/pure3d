from helpers.files import readYaml
from helpers.messages import error


class Users:
    def __init__(self, Config):
        self.Config = Config

    def getTestUsers(self):
        Config = self.Config
        yamlDir = Config.yamlDir

        testUsers = readYaml(f"{yamlDir}/testusers.yaml")
        userNameById = {}
        userRoleById = {}
        testUserIds = set()

        for (name, info) in testUsers.items():
            userId = info["id"]
            if userId in testUserIds:
                prevName = userNameById[userId]
                error(f"WARNING: duplicate test user {userId} = {name}, {prevName}")
                continue
            testUserIds.add(userId)
            userNameById[userId] = name
            userRoleById[userId] = info["role"]

        return dict(
            testUserIds=testUserIds, userNameById=userNameById, userRoleById=userRoleById
        )

    def getPermissions(self):
        Config = self.Config
        yamlDir = Config.yamlDir

        authData = readYaml(f"{yamlDir}/authorise.yaml")
        return authData

    def getUserProject(self):
        Config = self.Config
        yamlDir = Config.yamlDir

        projectUsers = readYaml(f"{yamlDir}/projectusers.yaml")

        userProjects = {}
        for (project, users) in projectUsers.items():
            for (user, role) in users.items():
                userProjects.setdefault(user, {})[project] = role
        return dict(projectUsers=projectUsers, userProjects=userProjects)
