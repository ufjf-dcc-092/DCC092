class MulticastController:

    def __init__(self, serverIPAddress, serverMAC, serverPort):
        self.members = []
        self.serverIPAddress = serverIPAddress
        self.serverMAC = serverMAC
        self.serverPort = serverPort

    def addMember(self,member):
        if (not self.hasMember(member)):
            self.members.append(member)

    def removeMember(self,member):
        self.members.remove(member)

    def getMembers(self):
        return self.members

    def getServerIPAddress(self):
        return self.serverIPAddress
    
    def getServerMAC(self):
        return self.serverMAC

    def getServerPort(self):
        return self.serverPort

    def hasMember(self, member):
        for m in self.members:
            if(m.id == member.id):
                return True
        return False
