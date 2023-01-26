import os, sys, csv, random
import ga_crossover as ga_c
import ga_mutation as ga_m

FIRST_INDEX = 2
LAST_INDEX = 5
INITIAL_POP = 100

def readFile():
	file = open('TS_Distances_Between_Cities.csv')
	csvreader = csv.reader(file)
	header = next(csvreader)
	rows = []
	rows.append(header)
	for row in csvreader:
	    rows.append(row)
	rows.pop()
	file.close()
	return rows

def generateRandomArrays(arr, count):
	generated_arr = []

	while len(generated_arr) < count:
		random_arr = random.sample(arr, len(arr))
		if arr not in generated_arr:
			generated_arr.append(random_arr)
			#print(random_arr)
	return generated_arr

def findDistanceOfCities(arr):
	start = arr[0]
	sum_distance = 0
	for num in range(1, len(arr)):
		sum_distance += int(rows[arr[num-1]][arr[num]])
	return sum_distance

def geneticAlgo(population, distance_list):
	# compare each adjacent neighbor's distance to each other
	# and remove the higher distance of the two and 
	# the corresponding array
	# fitness + selection
	termination = False
	most_fit = []
	smallest_distances = []
	for i in range(0, len(distance_list), 2):
		if distance_list[i] < distance_list[i+1]:
			smallest_distances.append(distance_list[i])
			most_fit.append(population[i])
		else:
			smallest_distances.append(distance_list[i+1])
			most_fit.append(population[i+1])

	#debug
	# print("most fit")
	# for i in most_fit:
	# 	print(i)
	# print("distances of most fit")
	# print(smallest_distances)

	# crossover and mutation
	crossover_arr = []
	for i in range(0, len(most_fit), 2):
		if (i+1 < len(most_fit)):
			arr = ga_c.crossover(most_fit[i], most_fit[i+1], FIRST_INDEX, LAST_INDEX)
			crossover_arr.append(arr)

	#debug
	# print("crossover")
	# for i in crossover_arr:
	# 	print(i)

	for arr in crossover_arr:
		arr = ga_m.mutation(arr)

	# print("mutation")
	# for i in crossover_arr:
	# 	print(i)

	# fitness of new mutations
	mutation_distances = []
	for args in crossover_arr:
		distance = findDistanceOfCities(args)
		mutation_distances.append(distance)

	# #debug
	# print("mutation distances")
	# print(mutation_distances)

	# replace worst ranking of population with new mutations
	length = len(mutation_distances)

	for i in range(0, len(distance_list)):
		for mutation_distance in mutation_distances:
			if distance_list[i] > mutation_distance:
				distance_list[i] = mutation_distance
				mutation_distances.remove(mutation_distance)
				population[i] = crossover_arr.pop(0)

	if (len(mutation_distances) == length):
		termination = True
	#	print("list is already efficient")			
	else:
		termination = False
	#	print("ready for another round")

	return termination, population, distance_list

	# print("new population")
	# for i in population:
	# 	print(i)
	# print("new distance list")
	# print(distance_list)

# ---- MAIN PROGRAM ----
rows = readFile()
arr = [1, 2, 3, 4, 5, 6, 7, 8]
min_distance = sys.maxsize

# generate random population and distances of cities
population = generateRandomArrays(arr, INITIAL_POP)
distance_list = []
for args in population:
	distance = findDistanceOfCities(args)
	distance_list.append(distance)

#debug
print("population")
for i in population:
	print(i)
print("distance of cities")
print(distance_list)

# LOOP BEGINS HERE
terminated = False
iterations = 0

while(terminated == False):
	terminated, population, distance_list = geneticAlgo(population, distance_list)
	iterations += 1


#debug
print("new population")
for i in population:
	print(i)
print("new distance of cities")
print(distance_list)
print("iterations")
print(iterations)

index = -1
for i in range(0, len(distance_list)):
	if distance_list[i] < min_distance:
		min_distance = distance_list[i]
		index = i

print(min_distance)
print(population[index])
city_order = population[index]
for i in range(0, 8):
	print("City", i+1, ":", rows[0][city_order[i]])

# print("Min Distance is", min_distance)
# print("Array:", min_arr)
# city_order = min_arr

# for city in city_order:
# 	print(rows[0][city] + " - ", end = "")
# print("")


# file = open("Michael_Nguyen_GA_TS_Result.txt", "w") 
# file.write("Your text goes here") 
# file.close()

# choose initial population
# evaluate fitness of each individual in each population
# repeat

# [1,1] to [8,8]
# check
# [3, 5, 7, 2, 1, 6, 4, 8]
# [3, 3] + [3, 5] + [5, 7] + ... + [4, 8]

# [2, 5, 7, 6, 8, 1, 4, 3]

# divide = len(distance_list) // 2
# if divide % 2 == 1:
# 	divide -= 1

# distance_list = distance_list[:divide]

# print(distance_list)

