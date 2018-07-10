class MulticastController:

    def __init__(self):
        self.channelsIPs = ["1.1.1.1","2.2.2.2","3.3.3.3"]        
        self.members = [[] for x in range(3)]

    def addMember(self,member, channelIP):
        if (not self.hasMember(member, channelIP)):
            self.members[self.channelsIPs.index(channelIP)].append(member)

    def removeMember(self,member, channelIP):
        if(self.hasMember(member, channelIP)):
            self.members[self.channelsIPs.index(channelIP)].remove(member)

    def getMembers(self, channelIP):
        return self.members[self.channelsIPs.index(channelIP)]

    def hasMember(self, member, channelIP):
        if (member in self.members[self.channelsIPs.index(channelIP)]):
            return True
        else:
            return False
    
    def hasChannel(self, channelIP):
        if (channelIP in self.channelsIPs):
            return True
        else:
            return False
