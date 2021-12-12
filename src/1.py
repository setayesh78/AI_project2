import random
import statistics
import matplotlib.pyplot as plt
from collections import defaultdict
import time




class plot:
    def __init__(self, dictionary,succ_generation):
        self.dictionary = dictionary
        self.succ_generation = succ_generation
        
    def plotting(self):
        global METHOD
        global lev
        x = []
        minimum = []
        maximum = []
        average = []
        temp = []

        for i in self.dictionary:
            x.append(i)
            minimum.append(self.dictionary[i][0])
            maximum.append(self.dictionary[i][1])
            average.append(self.dictionary[i][2])
            
        plt.plot(x, minimum, label = "minimum")
        plt.plot(x, maximum, label = "maximum")
        plt.plot(x, average, label = "avarage")
        
        for i in self.succ_generation:
            temp.append(i)
            
        plt.plot(temp, self.succ_generation, 'r*')
        
        # naming the x axis
        plt.xlabel('x - generation')
        # naming the y axis
        plt.ylabel('y - fitness')
        plt.title("level : " + str(lev)+' _ method : '+str(METHOD))        
        plt.legend()
        plt.savefig('.\\src\\output\\'+str(lev)+'-'+str(METHOD)+'.png')
        plt.close()
        
        
class Individual(object):
    '''
    Class representing individual in population
    '''
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()
        self.population = population
        

    @classmethod
    def mutated_genes(self):
        '''
        create random genes for mutation
        '''
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_gnome(self):
        '''
        create chromosome or string of genes
        '''
        
        gnome_len = len(inpt)        
        lst = [self.mutated_genes() for _ in range(gnome_len)]
        return lst


    def mate(self, par2):
        '''
		Perform mating and produce new offspring
		'''

		# chromosome for offspring
        child_chromosome = []
        for i in range(0,int(len(self.chromosome)*0.4)):
            child_chromosome.append(self.chromosome[i])
        for i in range(int(len(self.chromosome)*0.4),len(par2.chromosome)):
            child_chromosome.append(par2.chromosome[i])
        return Individual(child_chromosome)




    def cal_fitness(self):
        '''
		Calculate fittness score, it is the number of
		characters in string which differ from target
		string.
		'''
        global WINPOINTS
        global inpt

        actions = self.chromosome        
        current_level = inpt
        steps = 0
        currentPoint=0
        maximumPoints =0
        maximumSteps =0
        for i in range(1,len(inpt)):
            current_step = current_level[i]
            if current_step == '_':
                steps += 1
                currentPoint += 1
                if actions[i - 1] == '0':
                    currentPoint+=1
                else:
                    currentPoint-=0.5
            elif current_step == 'G' :
                if i>1 and actions[i-2]=='1':
                    currentPoint+=2
                    steps += 1
                    currentPoint+=1
                elif actions[i - 1] == '1':
                    steps += 1
                    currentPoint+=1
                else:
                    if currentPoint>maximumPoints:
                        maximumSteps=steps
                        maximumPoints=currentPoint
                    steps=0
                    currentPoint=0
            elif current_step == 'L':
                if actions[i - 1] == '2':
                    steps += 1
                    currentPoint+=1
                else:
                    if currentPoint>maximumPoints:
                        maximumSteps=steps
                        maximumPoints=currentPoint
                    steps=0
                    currentPoint=0
            elif  current_step == 'M':
                if actions[i - 1] == '0' or actions[i - 1] == '2':
                    steps += 1
                    currentPoint+=2   

            #checking for GL
            if current_step=='L' and current_level[i-1]== 'G':
                if currentPoint>maximumPoints:
                    maximumSteps=steps
                    maximumPoints=currentPoint
                steps=0
                currentPoint=0
            if i==len(inpt)-1:
                ##todo: Does the presence of the enemy in the last house need to be investigated?
                steps+=1
                currentPoint+=1
                if current_step=='_' and actions[i]=='1':
                    currentPoint+=1
                if currentPoint>maximumPoints:
                    maximumSteps=steps
                    maximumPoints=currentPoint
                steps=0
                currentPoint=0
        if currentPoint>maximumPoints:
            maximumSteps=steps
            maximumPoints=currentPoint
        if WINPOINTS and maximumSteps == len(inpt):
            maximumPoints+=5
        return maximumPoints,maximumSteps

# Driver code
def main():
    global POPULATION_SIZE
    global population
    global MATE
    global CROSSOVER
	#current generation
    generation = 0
    new_generation = []
    new_population = []

    found = False
    counter=0
    avg1 = 0
	# create initial population
    population=[]
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))
    
    averageFitnesses = []
    plot_dict= defaultdict(list)
    succ_generation = []
    
    while not found:
        generation += 1
        population = sorted(population, key = lambda x:x.fitness[0], reverse=True)

        if population[0].fitness[1] == len(inpt):
            succ_generation.append(generation)
            

        #for i in range(0,len(population)): 
        #        print("number: {}\t string: {}\tfitness: {}\tsteps: {}".format(i+1,"".join(population[i].chromosome),population[i].fitness[0],population[i].fitness[1])) 

        #selection
        new_population = []
        if SELECTION==1:
            for i in range(0,POPULATION_SIZE//2): 
                new_population.append(population[i])   
                avg1+=new_population[i].fitness[0]
        elif SELECTION == 2:
            w=[]
            for i in range(0,len(population)): 
               w.append(population[i].fitness[0])
            new_population = random.choices(population, weights=tuple(w), k=POPULATION_SIZE//2)

        #Crossover
        s = len(new_population)
        new_generation = []
        new_generation.append(population[0])
        children = 0
        if CROSSOVER:    
            children = s
        else:
            children = s//2 

        for _ in range(children):
            parent1 = random.choice(new_population)
            parent2 = random.choice(new_population)
            child = parent1.mate(parent2)
            new_generation.append(child)
            if not CROSSOVER:
                new_generation.append(child)

                    

        #print("-------------------------------------------------------------------")    
        #for i in range(0,len(new_generation)): 
        #        print("number: {}\t string: {}\tfitness: {}\tsteps: {}".format(i+1,"".join(new_generation[i].chromosome),new_generation[i].fitness[0],new_generation[i].fitness[1]))    
        #Mutation
        for i in range(0,len(new_generation)): 
            if random.random() < MATE:
                r=random.randrange(len(new_generation[0].chromosome))
                if new_generation[i].chromosome[r] !='0':
                     new_generation[i].chromosome[r]='0'

        population=[]
        avg=0
        minimum = 10000
        maximum = 0
        #print("---------------------------------new generation----------------------------------*******")    
        for i in range(0,len(new_generation)): 
                #print("number: {}\t string: {}\tfitness: {}\tsteps: {}".format(i+1,"".join(new_generation[i].chromosome),new_generation[i].fitness[0],new_generation[i].fitness[1]))   
                population.append(new_generation[i])
                
                if new_generation[i].fitness[0] >= maximum:
                    maximum = new_generation[i].fitness[0]
                if new_generation[i].fitness[0] <= minimum:
                    minimum = new_generation[i].fitness[0]
                
                avg+=new_generation[i].fitness[0]
                
        avg/=len(new_generation)

        plot_dict[generation].append(minimum)
        plot_dict[generation].append(maximum)
        plot_dict[generation].append(avg)        
        counter+=1
   
            
        if (counter >= 2 and abs(plot_dict[generation][2] - plot_dict[generation-1][2]) < 0.02) or counter==100:
        #if (counter >= 2 and abs(statistics.mean(averageFitnesses) - avg) < 0.01) or counter==100:
            found=True
        averageFitnesses.append(avg)
    
        
    print(generation)
    plot(plot_dict,succ_generation).plotting()
    
    new_generation = sorted(new_generation, key = lambda x:x.fitness[0], reverse=True)
#    print("***************************************************************************************")    
#    print("number: {}\t string: {}\tfitness: {}\tsteps: {}".format(i+1,"".join(new_generation[i].chromosome),new_generation[0].fitness[0],new_generation[0].fitness[1]))   



######### CONFIG.
METHOD=2
POPULATION_SIZE = 200
WINPOINTS = True
SELECTION = 2
CROSSOVER = True #true: first method | false: second method
MATE = 0.1
if METHOD == 2:
    POPULATION_SIZE = 500
    WINPOINTS = False
    SELECTION = 1
    CROSSOVER = False #true: first method | false: second method
    MATE = 0.5

levels='.\\src\\input\\level'
#########

population = []
# Valid genes
GENES = "012"
lev=1
inpt = []

for i in range(1,11):
    file1 = open(levels+str(i)+'.txt', 'r')
    inpt = list(file1.read())
    
    start = time.time()
    
    main()

    end = time.time()
    print("convergence time : ")
    print(end-start)  
    
    print("========================== level : " + str(lev) + " ==============================")
    lev+=1




#if __name__ == '__main__':
    #global inpt
    #file1 = open(levels+'3'+'.txt', 'r')
    #inpt = list(file1.read())
    # Number of individuals in each generation