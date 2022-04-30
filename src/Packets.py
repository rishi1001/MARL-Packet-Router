class packet():

    def __init__(self,ttl):
        self.ttl=ttl

    def decrease_ttl(self):
        self.ttl-=1
        
    def get_ttl(self):
        return self.ttl