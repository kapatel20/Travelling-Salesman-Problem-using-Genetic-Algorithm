import time
import random

start = time.time()
  
def cleanFirst(s):
    return int(s.split("\n")[0])

def cleanIP(s1):
    ip=[]
    for i in s1:
        temp = []
        temp = i.split("\n")[0].split(" ")
        temp = [int(j) for j in temp]
        ip.append(temp)
    return ip


def createDict(totalCities, input):
    d = {}
    for i in range(totalCities):
        d[i] = input[i]
    return d

def CreateInitialPopulation(batch, cities):
    pop=[]
    for i in range(batch):
        temp = cities.copy()
        random.shuffle(temp)
        temp.append(temp[0])
        pop.append(temp)
    return pop

def distance(cityA, cityB):
    return (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 + (cityA[2]-cityB[2])**2

def fitnessFunction(cities,location_dict,mat):
    fitness = 0
    for i in range(0,len(cities)-1):
        fitness += mat[cities[i]][cities[i+1]]
    return fitness

def calFitness(population_list,location_dict,mat):
    pop_fitness= []
    for i in population_list:
        temp = fitnessFunction(i,location_dict,mat)
        pop_fitness.append(temp)
    return pop_fitness

def calFitnessSum(population_fitness):
    return sum(population_fitness)

def distMatrix(loc):
    l = list(loc.keys())
    mat = [[0 for x in range(len(l))] for y in range(len(l))]
    for i in range(len(l)):
        for j in range(i,len(l)):
            if i==j:
                continue

            dist = distance(loc[i],loc[j])
            mat[i][j] = dist
            mat[j][i] = dist
    return mat


def normalize(population_fitness):
    fitnessTotalSum = calFitnessSum(population_fitness)
    for i in range(len(population_fitness)):
        population_fitness[i]=fitnessTotalSum/population_fitness[i]
    return population_fitness


def createSortedList(population_fitness,population_list):
    fitPopList = []
    for i in range(len(population_fitness)):
        temp_list = [population_fitness[i],population_list[i]]
        fitPopList.append(temp_list)

    fitPopList.sort(key = lambda x:x[0],reverse=True)
    return fitPopList

def parentSelection(fitnessPopList, pop_fitness_list):
    s = calFitnessSum(pop_fitness_list)
    r = random.random()*s
    i=0
    while i<len(fitnessPopList) and r<s:
        r+=fitnessPopList[i][0]
        i+=1
        if i==len(fitnessPopList)-1:
            i=0
    return fitnessPopList[i-1][1]

def newPopulation(old,elite_pop):
    new = []
    for i in range(elite_pop):
        new.append(old[i][1])
    return new

def reproduction(parentX, parentY):
    start = random.randint(0,len(parentX)-2)
    end = random.randint(start,len(parentX)-2)
    
    child = []
    for i in range(start,end+1):
        child.append(parentX[i])
    
    d={}
    for i in parentY:
        d[i]=True
    
    for i in child:
        d[i]=False
    
    for i in range(len(parentY)):
        if d[parentY[i]]:
            child.append(parentY[i])
            d[parentY[i]]=False
    child.append(child[0])
    return child 

def mutation(child):
    random_number =random.random()
    if(random_number<=0.01):
        ind1 = random.randint(1,numOfCities-1)
        ind2 = random.randint(1,numOfCities-1)
        child[ind1],child[ind2] = child[ind2],child[ind1]
        child[-1] = child[0]
    return child

def crossOver(old_fitness_population_list,fitness_list_norm, elite_pop, regular_pop):
    new_population = newPopulation(old_fitness_population_list,elite_pop)
    for i in range(int(regular_pop)//2):
        parentM = parentSelection(old_fitness_population_list, fitness_list_norm)
        parentF = parentSelection(old_fitness_population_list, fitness_list_norm)
        child1 = reproduction(parentM, parentF)
        child2 = reproduction(parentF, parentM)
        
        child1 = mutation(child1)
        child2 = mutation(child2)
        
        new_population.append(child1)
        new_population.append(child2)
    return new_population

def outputAnswer(ans,loc):
    with open('output.txt','w') as f:
        for i in range(len(ans)):
            temp = loc[ans[i]]
            temp = [str(k) for k in temp]
            f.write(str(" ".join(temp)))
            if i!=len(ans)-1:
                f.write("\n")



#Input from the text file
with open('input.txt') as f:
    lines = f.readlines()

# numOfCities - Number of Cities
numOfCities = cleanFirst(lines[0])
lines.pop(0)

# batch_size - size of population
batch_size = min(450,numOfCities*10)
# batch_size = 10

# input - contains coordinates of cities
ip = cleanIP(lines)

#Contains dictionary of cities:coordinates
location = createDict(numOfCities,ip)
# print(location)

#Population created from cities
population = [i for i in range(numOfCities)]
population = CreateInitialPopulation(batch_size,population)
# print(population)

#Matrix containing distances
distanceMatrix = distMatrix(location)

#List of fitness for all population elements
fitness_list = calFitness(population,location,distanceMatrix)
# print(fitness_list)

#Containes normalized fitness_list of population
fitness_list_normalized = normalize(fitness_list)

#CreateList of list containing fitness-population pair
fitness_population_list = createSortedList(fitness_list_normalized,population)
# print(fitness_population_list)

#Number of iterations
iteration = 0

#max number of iterations
if numOfCities<200:
    max_iterations = 1500
elif numOfCities<=500:
    max_iterations = 1250
else:
    max_iterations = 750

#contains final answer
final_answer = fitnessFunction(fitness_population_list[0][1],location,distanceMatrix)

#print(final_answer)
#contains answer path
answer_path = fitness_population_list[0][1]

elite_pop = int(len(fitness_population_list)*0.20)
regular_pop = int(len(fitness_population_list)-elite_pop)

early_stopping = 0
max_wait=250
    
while iteration<max_iterations and early_stopping<max_wait and time.time()-start<195:
    population = crossOver(fitness_population_list,fitness_list_normalized,elite_pop,regular_pop)
    fitness_list = calFitness(population,location,distanceMatrix)
    fitness_list_normalized = normalize(fitness_list)
    fitness_population_list = createSortedList(fitness_list_normalized,population)
    first_ele_distance = fitnessFunction(fitness_population_list[0][1],location,distanceMatrix)
    if final_answer>first_ele_distance:
        final_answer = first_ele_distance
        answer_path = fitness_population_list[0][1]
        early_stopping=0
    else:
        early_stopping+=1
    
    iteration+=1

outputAnswer(answer_path,location)




    





