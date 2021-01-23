import client
import ast
import random

class Agent: 
    def __init__(self):
        self.c = client.Client('127.0.0.1', 50001)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.goalNodePos =(0,0)
        self.state = (0,0)
        self.maxCoord = ast.literal_eval(self.c.execute("info", "maxcoord"))
        self.rewardRecieved = 0
        self.qLearningTable = {}

    def getConnection(self):
        return self.res

    #Retorna a posição atual do agente no mundo
    def getSelfPosition(self):
        return ast.literal_eval(self.c.execute("info", "position"))

    #Retorna a posição do goal
    def getGoalPosition(self):
        return ast.literal_eval(self.c.execute("info", "goal"))
    
    #Retorna um dicionário com todas as rewards de cada posição
    def getRewards(self):
        return ast.literal_eval(self.c.execute("info", "rewards"))
    
    def markArrow(self, direction, x, y):
        if direction == 0:
            self.c.execute("marrow", "north" + "," + str(y) + "," + str(x))
        elif direction == 1:
            self.c.execute("marrow", "south" + "," + str(y) + "," + str(x))
        elif direction == 2:
            self.c.execute("marrow", "east" + "," + str(y) + "," + str(x))
        else:
            self.c.execute("marrow", "west" + "," + str(y) + "," + str(x))


# Visto que temos a tabela com todas as rewards tudo o que temos de fazer
# é identificar o index correspondente à posição no mapa e assim fazer os
# calculos das rewards usando RL /Qlearning
# Formula de recompensa = pontosPosicaoAtras + 0.9 * (pontosPosicaoAtual)

    def randomSearch(self):
        states = ["north", "east", "west", "south"]
        number = 0
        goalPosition = self.getGoalPosition()
        positionsArray = []

        self.rewards = self.getRewards()
        self.initializeTable()
        while number != 100:
            state = random.randint(0,3)   
            self.c.execute("command", states[state])
            positionsArray.append(self.getSelfPosition())
            if self.getSelfPosition() == goalPosition:
                self.c.execute("command", "home")
                self.updateQLearningTable(positionsArray)
                positionsArray = []
                number += 1
        print(self.qLearningTable)
        self.drawArrows()
        input("")

# Irá proceder à atualização das pontuações na tabela de QLearning usando a formula
# recompensa = pontosPosicaoAtras + 0.9 * (pontosPosicaoAtual)

    def updateQLearningTable(self, positionsArray):
        for i in range(len(positionsArray) -1, -1,-1):
            if self.rewards[positionsArray[i][0]][positionsArray[i][1]] == 0:
                if positionsArray[i][1] == (positionsArray[i+1][1] +1) :
                    self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][0] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                    self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                elif positionsArray[i][1] == (positionsArray[i+1][1] -1) :
                    self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][1] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                    self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                elif positionsArray[i][0] == (positionsArray[i+1][0] -1) :
                    self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][2] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                    self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                elif positionsArray[i][0] == (positionsArray[i+1][0] +1) :
                    self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][3] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                    self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
            elif self.rewards[positionsArray[i][0]][positionsArray[i][1]] > 0 and self.rewards[positionsArray[i][0]][positionsArray[i][1]] != 100 :
               if (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]]) > self.rewards[positionsArray[i][0]][positionsArray[i][1]]:
                    if positionsArray[i][1] == (positionsArray[i+1][1] +1) :
                        self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][0] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                        self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                    elif positionsArray[i][1] == (positionsArray[i+1][1] -1) :
                        self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][1] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                        self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                    elif positionsArray[i][0] == (positionsArray[i+1][0] -1) :
                        self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][2] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                        self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                    elif positionsArray[i][0] == (positionsArray[i+1][0] +1) :
                        self.qLearningTable[(positionsArray[i][0], positionsArray[i][1])][3] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
                        self.rewards[positionsArray[i][0]][positionsArray[i][1]] = (0.9 * self.rewards[positionsArray[i+1][0]][positionsArray[i+1][1]])
    def initializeTable(self):
        for x in range(self.maxCoord[0]):
            for y in range(self.maxCoord[1]):
                self.qLearningTable[(x,y)] = [0,0,0,0]
        

    def drawArrows(self):
        list = [(0,0), (1,0), (2,0), (2,1), (3,0), (4,0), (5,0), (6,0) , (7,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4), (3,4), (4,4), (5,4), (6,4),
        (7,1), (7,2), (7,3), (7,4)]
        for x, y in self.qLearningTable:
            if (x,y) not in list:
                index1 = self.qLearningTable[(x,y)].index(max(self.qLearningTable[(x,y)]))
                self.markArrow(index1, x, y)




def main():
    agent = Agent()
    if agent.getConnection() != -1:
        agent.randomSearch()
    
if __name__ == "__main__":
    main()