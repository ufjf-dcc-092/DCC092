class MulticastGroupController:

    def __init__(self):
        self.members = []

    def addMember(self,member):
        self.members.append(member)

    def removeMember(self,member):
        self.members.remove(member)

    def getMembers(self):
        return self.members
