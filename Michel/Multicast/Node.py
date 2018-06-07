class Node:

    def __init__(self ,id, isHost):
        self.isHost = isHost
        self.id = id

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        return self.id == other.id
            

        