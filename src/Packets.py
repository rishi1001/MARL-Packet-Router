class packet():

    def __init__(self,ttl):
        self.ttl=ttl
        self.path = []

    def decrease_ttl(self):
        self.ttl-=1
        
    def get_ttl(self):
        return self.ttl
    
    def getPath(self):
        return self.path
    
    def addToPath(self, x,y):
        self.path.append((x,y))