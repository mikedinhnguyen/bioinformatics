import random

def mutation(arr):
	# picks two random points
	first_point = random.randint(0, 7)
	second_point = first_point
	while (second_point == first_point):
		second_point = random.randint(0, 7)
		
	# swap value in array according to random point indices
	temp = arr[first_point]
	arr[first_point] = arr[second_point]
	arr[second_point] = temp
