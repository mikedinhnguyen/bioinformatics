import sys, os, csv, random, statistics
import ga_crossover as ga_c
import ga_mutation as ga_m

INITIAL_POP = 100
FIRST_INDEX = 2
LAST_INDEX = 5

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
	return generated_arr

def findDistanceOfCities(arr, rows):
	start = arr[0]
	sum_distance = 0
	for num in range(1, len(arr)):
		sum_distance += int(rows[arr[num-1]][arr[num]])
	return sum_distance

def geneticAlgo(rows, population, distance_list):
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
		elif distance_list[i] > distance_list[i+1]:
			smallest_distances.append(distance_list[i+1])
			most_fit.append(population[i+1])
		# else if they are the same, move on

	subset_len = len(most_fit)
	# crossover (I'm using Order 1 Crossover from the lecture)
	crossover_arr = []
	for i in range(0, len(most_fit), 2):
		if (i+1 < len(most_fit)):
			arr = ga_c.crossover(most_fit[i], most_fit[i+1], FIRST_INDEX, LAST_INDEX)
			arr2 = ga_c.crossover(most_fit[i+1], most_fit[i], FIRST_INDEX, LAST_INDEX)
			crossover_arr.append(arr)
			crossover_arr.append(arr2)

	# mutation (reorders two random places on the array, also taken from the lecture)
	for arr in crossover_arr:
		arr = ga_m.mutation(arr)

	# fitness of new mutations
	mutation_distances = []
	for args in crossover_arr:
		distance = findDistanceOfCities(args, rows)
		mutation_distances.append(distance)

	# replace worst ranking of population with new mutations
	length = len(mutation_distances)

	for i in range(0, len(distance_list)):
		for mutation_distance in mutation_distances:
			if distance_list[i] > mutation_distance:
				distance_list[i] = mutation_distance
				mutation_distances.remove(mutation_distance)
				population[i] = crossover_arr.pop(0)

	# termination happens when we can no longer replace any individual in the population with our mutations at all
	if (len(mutation_distances) == length):
		termination = True		
	else:
		termination = False

	# average
	average_sum = 0
	for distance in distance_list:
		average_sum += distance
	average = average_sum / len(distance_list)

	# median
	median_list = distance_list
	median_list.sort()
	median = median_list[len(median_list) // 2]

	# std
	std = statistics.stdev(distance_list)

	return termination, population, distance_list, average, median, std, subset_len

def writeToFile(iterations, average, median, std, subset_len, size):
	file = open("Michael_Nguyen_GA_TS_Info.txt", "a+") 
	file.write(str(iterations))
	file.write(". Population Size: ")
	file.write(str(size))
	file.write(" for iteration ")
	file.write(str(iterations))
	file.write("\n")
	file.write("Average fitness score = ")
	file.write(str(average))
	file.write("\n")
	file.write("Median fitness score = ")
	file.write(str(median))
	file.write("\n")
	file.write("STD of fitness scores = ")
	file.write(str(std))
	file.write("\n")
	file.write("Size of the selected subset of the population = ")
	file.write(str(subset_len))
	file.write("\n\n")
	file.close()

def main():
	rows = readFile()
	arr = [1, 2, 3, 4, 5, 6, 7, 8]
	min_distance = sys.maxsize

	# generate random population and distances of cities
	population = generateRandomArrays(arr, INITIAL_POP)
	distance_list = []
	for args in population:
		distance = findDistanceOfCities(args, rows)
		distance_list.append(distance)

	terminated = False
	iterations = 0
	file = open("Michael_Nguyen_GA_TS_Info.txt", "w") 
	file.close()

	# LOOP BEGINS HERE
	while(terminated == False):
		terminated, population, distance_list, average, median, std, subset_len = geneticAlgo(rows, population, distance_list)
		iterations += 1
		writeToFile(iterations, average, median, std, subset_len, INITIAL_POP)

	index = -1
	for i in range(0, len(distance_list)):
		if distance_list[i] < min_distance:
			min_distance = distance_list[i]
			index = i

	city_order = population[index]

	file = open("Michael_Nguyen_GA_TS_Result.txt", "w") 
	for i in range(0, 8):
		file.write("City ")
		file.write(str(i+1))
		file.write(": ")
		file.write(str(rows[0][city_order[i]]))
		file.write("\n")
	file.close()

	print("text files are done writing")

if __name__ == "__main__":
	main()
	