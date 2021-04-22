import random
import numpy as np
N = 0
popSize = 0
population = []

# class 'Individual' is inspired by Dr. Nisha's genetic_algorithm.py class example

class Individual(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calc_fitness()

    def calc_fitness(self):
        fit = self.check_for_vert_hor_attacks()
        fit += self.check_for_diag_attacks()
        return fit

    # check_for_diag_attacks was inspired by techniques found in
    # "Computing number of conflicting pairs in N-Queen board in Linear Time and Space Complexity"
    # By Tanvir Sojal at:
    # https://towardsdatascience.com/computing-number-of-conflicting-pairs-in-a-n-queen-board-in-linear-time-and-space-complexity-e9554c0e0645
    def check_for_diag_attacks(self):
        number_of_attacks = 0

        # check primary diagonals
        xy_sum = []
        for index_y, y in enumerate(self.chromosome):
            for index_x, x in enumerate(y):
                if x == 1:
                    xy_sum.append(index_x + index_y)
        for x in xy_sum:
            if xy_sum.count(x) > 1:
                number_of_attacks += 1
        xy_sum.clear()

        # check secondary diagonals
        for index_y, y in enumerate(self.chromosome):
            for index_x, x in enumerate(y):
                if x == 1:
                    xy_sum.append((len(self.chromosome) - index_x) + index_y)
        for x in xy_sum:
            if xy_sum.count(x) > 1:
                number_of_attacks += 1

        return number_of_attacks

    def check_for_vert_hor_attacks(self):
        number_of_attacks = 0
        # check for horizontal attacks
        for x in self.chromosome:
            if x.count(1) > 1:
                number_of_attacks += x.count(1)

        # check for vertical attacks
        y = 0
        for x in self.chromosome:
            y_row = []
            for x1 in self.chromosome:
                y_row.append(x1[y])
            if y_row.count(1) != 1:
                number_of_attacks += y_row.count(1)
            y += 1

        return number_of_attacks

    def mate(self, mate):
        crossover_point = int(len(self.chromosome) / 2)

        rotated1 = np.rot90(self.chromosome, 1)
        rotated2 = np.rot90(mate.chromosome, 1)

        # Swap the the first half of one list onto the first half of the other list, and vise versa
        for x in range(crossover_point):
            temp = rotated1[x].copy()
            rotated1[x] = rotated2[x]
            rotated2[x] = temp

        # there is a 50 percent chance of genetic abnormality
        if random.random() <= .5:
            i = random.choice(range(N))
            i2 = random.choice(range(N))
            for x in range(N):
                rotated1[i][x] = 0
                rotated1[i2][x] = 0

            rotated1[i][i2] = 1
            rotated1[i2][i] = 1
        # see above comment, same applies for the second child
        if random.random() <= .5:
            i = random.choice(range(N))
            i2 = random.choice(range(N))
            for x in range(N):
                rotated2[i][x] = 0
                rotated2[i2][x] = 0
            rotated2[i][i2] = 1
            rotated2[i2][i] = 1

        rotated1 = np.rot90(rotated1, 3)
        rotated2 = np.rot90(rotated2, 3)

        list1 = rotated1.tolist()
        list2 = rotated2.tolist()

        children = [Individual(list1), Individual(list2)]
        return children

    def print_individual(self):
        for x in self.chromosome:
            print(x)

    @classmethod
    def create_gnome(self):
        # create a board
        # there will be only one queen per column
        global N
        columns = list(range(N))
        board = [[0 for x in range(N)] for x in range(N)]

        for x in board:
            x = random.choice(columns)
            columns.remove(x)
            board[random.choice(range(N))][x] = 1
        return board


def check_for_solution():
    if population[0].fitness == 0:
        return True
    else:
        return False
# ------------------------------------------------driver code------------------------------------------------ #


N = int(input("How many queens would you like on the board?\n"))
while N < 1:
    N = int(input("Enter a number greater than 0, preferably 1 or greater than 3, otherwise you will see this message "
                  "again, or it will never find a solution\n"))
popSize = int(input("What should the population size be?\n"))
# If the user specifies a population size lower than 4, the program self destructs *BOOM* (╯°□°）╯︵ ┻━┻
# Idk why you would, with a population size that low it would take forever to find a solution!
while popSize < 4:
    popSize = int(input("Please enter a number greater than four.\n"))

# print a visual of what the board will look like
# just so the user doesnt have a panic attack when they don't know whats going on.
board = [[0 for x in range(N)] for x in range(N)]
for i, x in enumerate(board[0]):
    board[0][i] = 1
print("\nYour board will look like:")
for x in board:
    print(x)
print("1s represent queens, 0s represent blank spaces\n")


# okay, now that the user knows whats going on, lets do the heavy lifting

for x in range(popSize):
    population.append(Individual(Individual.create_gnome()))
# sort population by fitness value
population.sort(key= lambda individual : individual.fitness)

generation = 1

if not check_for_solution():
    while not check_for_solution():
        # the least fit half of the population dies off
        half = int(len(population) / 2)
        population = population[:half]
        # because mating creates two children, only run the parent.mate() function for popSize/4 times
        for x in range(int(half/2)):
            # Two parents are randomly selected
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            # parents are then mated, and their children are added to the population
            population.extend(parent1.mate(parent2))
        # sort the generation by fitness level
        population.sort(key=lambda individual: individual.fitness)
        generation += 1
        print("\nbest of generation " + str(generation) + " at fiteness level " + str(population[0].fitness) + ":")
        # print the best individual in the population for the current generation
        for x in population[0].chromosome:
            print(x)
        print("population size: " + str(len(population)))

print("\na solution is:")
for x in population[0].chromosome:
    print(x)
print("\nIt took " + str(generation) + " generation(s) to find this solution")
