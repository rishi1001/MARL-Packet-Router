import random

# generate map of size n*m 
## p is probability of getting a Uav at particular cell
class generate_map():
    def __init__(self,n,m,p):
        self.n=n
        self.m=m
        self.p=p
    def generate(self):
        map=[['-' for i in range(self.m)] for j in range(self.n)]
        x=random.randint(0,self.n-1)
        y=random.randint(0,self.m-1)
        map[x][y]='B'
        for i in range(self.n):
            for j in range(self.m):
                x=random.uniform(0,1)
                if(x<=self.p):
                    map[i][j]='U'
                else:
                    map[i][j]='I'
        return map  