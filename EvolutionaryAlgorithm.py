from copy import deepcopy
import random

# grids

grid1 =[[3,0,0,0,0,5,0,4,7],
        [0,0,6,0,4,2,0,0,1],
        [0,0,0,0,0,7,8,9,0],
        [0,5,0,0,1,6,0,0,2],
        [0,0,3,0,0,0,0,0,4],
        [8,1,0,0,0,0,7,0,0],
        [0,0,2,0,0,0,4,0,0],
        [5,6,0,8,7,0,1,0,0],
        [0,0,0,3,0,0,6,0,0]]

grid2 =[[0,0,2,0,0,0,6,3,4],
        [1,0,6,0,0,0,5,8,0],
        [0,0,7,3,0,0,2,9,0],
        [0,8,5,0,0,1,0,0,6],
        [0,0,0,7,5,0,0,2,3],
        [0,0,3,0,0,0,0,5,0],
        [3,1,4,0,0,2,0,0,0],
        [0,0,9,0,8,0,4,0,0],
        [7,2,0,0,4,0,0,0,9]]

grid3 =[[0,0,4,0,1,0,0,6,0],
        [9,0,0,0,0,0,0,3,0],
        [0,5,0,7,9,6,0,0,0],
        [0,0,2,5,0,4,9,0,0],
        [0,8,3,0,6,0,0,0,0],
        [0,0,0,0,0,0,6,0,7],
        [0,0,0,9,0,3,0,7,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,6,0,0,0,0,1,0]]

# function to generate the population

def generate_candidates(startgrid, pop_size):

    # make a copy of the start grid (newgrid)
    # checking in the start grid where it's equal to 0
    # if it's equal to 0, we can replace the 0 with a random number
    # we make this change in the newgrid 

    candidates = []
    for x in range(pop_size):
        newgrid = deepcopy(startgrid)
        for i in newgrid:
            for j in range(len(i)):
                if i[j]==0:
                    i[j] = random.randint(1,9)
        candidates.append(newgrid)
    return candidates
  
# function to calculate the fitness of each candidate
    
def fitness(individual):

    # looking at how many duplicates are in a row (the fitness)
    # adding the fitness of each row to fitness_value_row

    fitness_value_row = 0 
    for i in individual:
        fitness_value_row+=(9 - len(set(i)))
    

    # looking at how many duplicates are in a column (the fitness)
    # adding the fitness of each column to fitness_value_column

    fitness_value_column = 0 
    for i in range(9):
        column=[]
        for j in individual:
            column.append(j[i])
        fitness_value_column += (9 - len(set(column)))
            

    # looking at how many duplicates are in a box (the fitness)
    # adding the fitness of each box to fitness_value_box

    fitness_value_boxes = 0
    boxes = []
    for i in range(0, 7, 3):
        boxes.append(individual[i][0:3] + individual[i+1][0:3] + individual[i+2][0:3])
        boxes.append(individual[i][3:6] + individual[i+1][3:6] + individual[i+2][3:6])
        boxes.append(individual[i][6:9] + individual[i+1][6:9] + individual[i+2][6:9])
    
    fitness_value_boxes = sum(9-len(set(box)) for box in boxes)

    # get the total fitness value of the candidate by summing the total fitness of values of its rows, columns and boxes.

    total_fitness_value = fitness_value_boxes + fitness_value_column + fitness_value_row

    return total_fitness_value

# function that selects two parents randomly in the list of population

def selection(population):

    parent1=random.choice(population)
    parent2=random.choice(population)

    return parent1,parent2
    
# crossover function with the two parents found in selection to find child

def crossover(parent1, parent2):

    # Initialize a child1 and a child2 list

    child1 = []
    child2 = []

    parent1 = [i for row in parent1 for i in row]
    parent2 = [j for row in parent2 for j in row]

    for parent_pair in zip(parent1,parent2):
        choice = random.randint(0,1)
        child1.append(parent_pair[choice])
        child2.append(parent_pair[abs(choice-1)])

    child1 = [child1[i:i + 9] for i in range(0, len(child1), 9)]
    child2 = [child2[i:i + 9] for i in range(0, len(child2), 9)]

    return child1, child2

# mutation function to mutate the child 

def mutation(child, startgrid, mutation_rate):

    # we define a random number between 0 and 1
    # for each number in the child grid, if the random number is smaller than the mutation rate, mutate the number
    # if random number greater, no mutation for the number in the child grid

    for i in range(9):
        for j in range(9):
            random_number = random.uniform(0,1)
            if startgrid[i][j] == 0:
                if(random_number < mutation_rate):
                    child[i][j] = random.randint(1,9)

    
    return child

# print out sudoku

def print_sudoku(candidate):
    
    for i in candidate:
        print(i)

# main run

if __name__ == "__main__":

    # asks user for which grid it would like to solve

    input_user = input("Enter 1 for grid1, 2 for grid2 or 3 for grid3: ")

    # solves for grid 1

    if input_user == "1":

        mutation_rate = 0.03
        size_of_population = 10000
        generation_limit = 1000

        # generate population

        population = generate_candidates(grid1, size_of_population)

        # sort population based on their fitness value
        # individual at index 0 will have the best fitness value out of all the population

        for y in range(generation_limit):
            population = sorted(population, key=lambda ind : fitness(ind), reverse = False)

            # best fitness value is 0 

            if fitness(population[0]) == 0:
                print("The solution to the sudoku is : ")
                print_sudoku(population[0])
                break

            print("Fitness value =", fitness(population[0]))
            print()
            print_sudoku(population[0])
            print()

            next_gen = []

            # if the best fitness value is 6, decrease the mutation rate

            if fitness(population[0])== 6:
                mutation_rate = 0.0002

            # if the best fitness value is 2, decrease the mutation rate

            if fitness(population[0])==2:
                mutation_rate = 0.00002

            # sort the parents of the selection

            for x in range(int(len(population)/2)):
                potential_parents = []
                for y in range(10):
                    parent1, parent2 = selection(population)
                    potential_parents.append(parent1)
                    potential_parents.append(parent2)
                
                potential_parents = sorted(potential_parents, key=lambda ind : fitness(ind), reverse = False)
                winner1 = potential_parents[0]
                winner2 = potential_parents[1]

                # find the children

                children = crossover(winner1,winner2)

                # mutate the children

                mutated_child1 = mutation(children[0], grid3, mutation_rate)
                mutated_child2 = mutation(children[1], grid3, mutation_rate)

                # pass the children on to the next generation

                next_gen += [mutated_child1, mutated_child2]

            population = next_gen

    # solves for grid 2
            
    elif input_user == "2":

        rate = 0.2
        mutation_rate = 0.03
        size_of_population = 10000
        generation_limit = 1000
        population = generate_candidates(grid2, size_of_population)


        for y in range(generation_limit):
            population = sorted(population, key=lambda ind : fitness(ind), reverse = False)

            

            if fitness(population[0]) == 0:
                print("The solution to the sudoku is : ")
                print_sudoku(population[0])
                break

            print("Fitness value =", fitness(population[0]))
            print()
            print_sudoku(population[0])
            print()

            next_gen = []

            if fitness(population[0])==24:
                rate = 0.5

            if fitness(population[0])== 6:
                mutation_rate = 0.0002

            if fitness(population[0]) == 2:
                mutation_rate = 0.00002
                
            

            for x in range(int(len(population)/2)):
                potential_parents = []
                for y in range(10):
                    parent1, parent2 = selection(population)
                    potential_parents.append(parent1)
                    potential_parents.append(parent2)
                
                potential_parents = sorted(potential_parents, key=lambda ind : fitness(ind), reverse = False)
                winner1 = potential_parents[0]
                winner2 = potential_parents[1]

                children = crossover(winner1,winner2)
                mutated_child1 = mutation(children[0], grid3, mutation_rate)
                mutated_child2 = mutation(children[1], grid3, mutation_rate)
                next_gen += [mutated_child1, mutated_child2]

            population = next_gen

    # solves grid 3

    else:

        rate = 0.2
        mutation_rate = 0.04
        size_of_population = 10000
        generation_limit = 1000
        population = generate_candidates(grid3, size_of_population)


        for y in range(generation_limit):
            population = sorted(population, key=lambda ind : fitness(ind), reverse = False)

            

            if fitness(population[0]) == 0:
                print("The solution to the sudoku is : ")
                print_sudoku(population[0])
                break

            print("Fitness value =" , fitness(population[0]))
            print()
            print_sudoku(population[0])
            print()
            
            
            next_gen = []

            if fitness(population[0])==24:
                rate = 0.5

            if fitness(population[0])== 6:
                mutation_rate = 0.0002
            
            if fitness(population[0])==2:
                mutation_rate = 0.00002

            

            for x in range(int(len(population)/2)):
                potential_parents = []
                for y in range(10):
                    parent1, parent2 = selection(population)
                    potential_parents.append(parent1)
                    potential_parents.append(parent2)
                
                potential_parents = sorted(potential_parents, key=lambda ind : fitness(ind), reverse = False)
                winner1 = potential_parents[0]
                winner2 = potential_parents[1]

                children = crossover(winner1,winner2)
                mutated_child1 = mutation(children[0], grid3, mutation_rate)
                mutated_child2 = mutation(children[1], grid3, mutation_rate)
                next_gen += [mutated_child1, mutated_child2]

            population = next_gen
