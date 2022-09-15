import os

from users import getTestUsers, getPermissions, getUserProject
from projects import getProjectStatus

TEST_MODE = os.environ["flasktest"] == "test"


class Auth:
    def __init__(self):
        self.authData = getPermissions()
        self.userData = getTestUsers() if TEST_MODE else {}
        self.projectstatus = getProjectStatus()
        self.userProject = getUserProject()

    def auth(self, userId, projectId, action):
        authData = self.authData
        userData = self.userData
        projectStatus = self.projectStatus
        userProject = self.userProject

        userRole = userData.get(userId, None)
        projectRole = (
            None if userRole is None else userProject.get(projectId, {}).get(userId, None)
        )
        projectPub = "published" if projectStatus.get(projectId, False) else "unpublished"

        projectRules = authData["projectrules"][projectPub]
        condition = (
            projectRules[userRole] if userRole in projectRules else projectRules[None]
        ).get(action, False)
        permission = condition if type(condition) is bool else projectRole in condition
        return permission
