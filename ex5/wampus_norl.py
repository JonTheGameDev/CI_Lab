class Person:
    def __init__(self,size):
        self.size=size
        self.pos=[size-1,0]
        self.sense={"Stench":False,"Breeze":False,"Glitter":False,"Bump":False,"Scream":False}
        self.dead=False
        self.foundwampus=False
        self.memory=[]
        for i in range(size):
            self.memory.append([])
            for j in range(size):
                self.memory[i].append([])
        self.memory[size-1][0].extend(["OK","A","V"])
        self.memory[size-2][0].append("OK")
        self.memory[size-1][1].append("OK")
        self.fixed={}
    def display(self):
        for i in range(self.size):
            print("--------------"*self.size+"-")
            for j in range(5): 
                for k in range(self.size):
                    if j==0:
                        print("|",f"{k+1},{self.size-i}"," "*8,end="")
                    elif j==2 and self.memory[i][k]:
                        print("|",f"{','.join(self.memory[i][k]):<12}",end="")
                    else:
                        print("|"," "*12,end="")
                print("|")
        print("--------------"*self.size+"-")
class Board:
    def __init__(self,size):
        self.size=size
        self.state=[]
        for i in range(size):
            self.state.append([])
            for j in range(size):
                self.state[i].append([])
        self.p=Person(self.size)
        self.threatpos=[]
    def display(self):
        for i in range(self.size):
            print("--------------"*self.size+"-")
            for j in range(5): 
                for k in range(self.size):
                    if j==2 and self.state[i][k]:
                        print("|",f"{','.join(self.state[i][k]):<12}",end="")
                    else:
                        print("|"," "*12,end="")
                print("|")
        print("--------------"*self.size+"-")
    def hasBumped(self,index,val,dir):
            if self.p.pos[index]==val:
                self.p.sense["Bump"]=True
                print("The agent bumped a wall")
                return True
            else: 
                self.p.memory[self.p.pos[0]][self.p.pos[1]].remove("A")
                self.p.pos[index]+=dir
                self.p.memory[self.p.pos[0]][self.p.pos[1]].append("A")
                if "V" not in self.p.memory[self.p.pos[0]][self.p.pos[1]]:
                    self.p.memory[self.p.pos[0]][self.p.pos[1]].append("V")
                return False
    def markDanger(self,pos,val,i,j,threat,danger):
        if pos!=val:
            if "OK" not in self.p.memory[i][j] and threat not in self.p.memory[i][j] and not (threat=="W?" and self.p.foundwampus):
                if "W" in self.p.memory[i][j] or "P" in self.p.memory[i][j] or (f"{i},{j}" in self.p.fixed and threat in self.p.fixed[f"{i},{j}"]):
                    return
                self.p.memory[i][j].append(threat)
                self.threatpos.append([i,j])
    def senseDanger(self,type,sense,threat,danger):
        x=self.p.pos[0]
        y=self.p.pos[1]
        l=self.state[x][y]
        c=0
        if type in l:
            self.p.sense[sense]=True
            if type not in self.p.memory[x][y]: self.p.memory[x][y].append(type)
            self.markDanger(x,0,x-1,y,threat,danger)
            self.markDanger(y,0,x,y-1,threat,danger)
            self.markDanger(x,self.size-1,x+1,y,threat,danger)
            self.markDanger(y,self.size-1,x,y+1,threat,danger)

        else: self.p.sense[sense]=False
    def removeFalseDanger(self,pos,val,i,j,threat):
        if pos!=val:
            if threat in self.p.memory[i][j]:
                self.p.memory[i][j].remove(threat)
                self.threatpos.remove([i,j])
                if f"{i},{j}" in self.p.fixed:
                    self.p.fixed[f"{i},{j}"].append(threat)
                else:
                    self.p.fixed[f"{i},{j}"]=[threat]
                return True
        return False
    def resolveDanger(self,type,threat,danger):
        x=self.p.pos[0]
        y=self.p.pos[1]
        l=self.state[x][y]
        if "OK" in self.p.memory[x][y] and type not in l :
            b1=self.removeFalseDanger(x,0,x-1,y,threat)
            b2=self.removeFalseDanger(y,0,x,y-1,threat)
            b3=self.removeFalseDanger(x,self.size-1,x+1,y,threat)
            b4=self.removeFalseDanger(y,self.size-1,x,y+1,threat)
            if b1 or b2 or b3 or b4:
                self.fixDanger(threat,danger)
    def checkDiagonals(self,pos1,val1,pos2,val2,i,j,type):
        if pos1!=val1 and pos2!=val2:
            if self.p.memory[i][j]==type:
                return 1
            return 0
        return 0
    def fixDanger(self,type,danger):
        for i in self.threatpos:
            x=i[0]
            y=i[1]
            if type not in self.p.memory[x][y]:
                continue
            c=self.checkDiagonals(x,0,y,0,x-1,y-1,type)+self.checkDiagonals(x,self.size-1,y,0,x+1,y-1,type)+self.checkDiagonals(x,0,y,self.size-1,x-1,y+1,type)+self.checkDiagonals(x,self.size-1,y,self.size-1,x+1,y+1,type)
            if c==0:
                self.p.memory[x][y].remove(type)
                self.threatpos.remove(i)
                if not self.p.memory[x][y]:
                    self.p.memory[x][y].append(danger)
                    if type=="W?":
                        self.p.foundwampus=True
    def fixOkTile(self,pos,val,i,j):
        if pos!=val:
            canfix=True
            for k in ["W?","P?","W","P","OK"]:
                if k in self.p.memory[i][j]:
                    canfix=False
            if canfix:        
                self.p.memory[i][j].append("OK")
    def inDanger(self,danger,name,threat):
        x=self.p.pos[0]
        y=self.p.pos[1]
        l=self.state[x][y]
        l2=self.p.memory[x][y]
        if danger in l:
            if threat in l2:
                l2.remove(threat)
                self.threatpos.remove([x,y])
                l2.append(danger)
            self.p.dead=True
            print("The Agent was killed by",name)
        else:
            if threat in l2:
                l2.remove(threat)
                self.threatpos.remove([x,y])
                if f"{x},{y}" in self.p.fixed:
                    self.p.fixed[f"{x},{y}"].append(threat)
                else:
                    self.p.fixed[f"{x},{y}"]=[threat]
                l2.append("OK")

    def foundGold(self):
        x=self.p.pos[0]
        y=self.p.pos[1]
        l=self.state[x][y]
        if "G" in l:
            self.p.sense["Glitter"]=True
            self.p.memory[x][y].append("G")
            print("The Agent has found the Gold!\nYOU WON")
    def newOkTile(self):
        x=self.p.pos[0]
        y=self.p.pos[1]
        l=self.state[x][y]
        self.fixOkTile(x,0,x-1,y)
        self.fixOkTile(y,0,x,y-1)
        self.fixOkTile(x,self.size-1,x+1,y)
        self.fixOkTile(y,self.size-1,x,y+1)
    def move(self,dir):
        if dir=="w":
            if self.hasBumped(0,0,-1):
                return self.p.sense
        if dir=="a":
            if self.hasBumped(1,0,-1):
                return self.p.sense
        if dir=="s":
           if self.hasBumped(0,self.size-1,1):
                return self.p.sense
        if dir=="d":
            if self.hasBumped(1,self.size-1,1):
                return self.p.sense
        self.p.sense["Bump"]=False
        self.resolveDanger("B","P?","P")
        self.resolveDanger("S","W?","W")
        self.senseDanger("B","Breeze","P?","P")
        self.senseDanger("S","Stench","W?","W")
        self.inDanger("P","Pitfall","P?")
        self.inDanger("W","Wambus","W?")
        self.foundGold()
        self.newOkTile()
        return self.p.sense
    def build(self):
        self.state[0][0].append("B")
        self.state[0][2].append("B")
        self.state[0][3].append("P")
        self.state[1][0].append("P")
        self.state[1][1].append("B")
        self.state[1][2].append("P")
        self.state[1][3].append("B")
        self.state[2][0].append("B")
        self.state[2][2].extend(["S","B","G"])
        self.state[3][1].append("S")
        self.state[3][2].append("W")
        self.state[3][3].append("S")

    def showPossible(self):
        i=self.p.pos[0]
        j=self.p.pos[1]
        print("Possible places to move: ",end="")
        if i!=0:
            print(f"Up({j+1},{self.size-i+1}) ",end="")
        if j!=0:
            print(f"Left({j},{self.size-i}) ",end="")
        if i!=self.size-1:
            print(f"Down({j+1},{self.size-i-1}) ",end="")
        if j!=self.size-1:
            print(f"Right({j+2},{self.size-i}) ",end="")
        print()
board=Board(4)
board.build()
print("State of Board")
board.display()
print("Agent's Initial Memory")
board.p.display()
print("Agents initial sense: Stench: None, Breeze: None, Glitter: None, Bump: None, Scream: None")
print("Welcome to WUMPUS WORLD!\nMove the agent up, down, left or right to reach the Gold and WIN!\nBut be weary of Pitfalls and the Ugly Wambus\n\n")
print("Enter the specific characters for movement:\n'w' - Up\n'a' - Left\n's' - Down\n'd' - Right")
options=["w","a","s","d"]
while(True):
    board.showPossible()
    op=input("Your option: ")
    if op not in options:
        print("invalid direction. Give again")
        continue
    senses=board.move(op)
    print("Agents sense after the move: ",f"Stench: {senses["Stench"]}, Breeze: {senses["Breeze"]}, Glitter: {senses["Glitter"]}, Bump: {senses["Bump"]}, Scream: {senses["Scream"]}")
    board.p.display()
    if board.p.dead or senses["Glitter"]:
        break