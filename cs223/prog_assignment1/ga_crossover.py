def crossover(parent1, parent2, first_point, last_point):
	# choose arbitrary part to copy over to child
	child = [0] * 8
	last_point += 1
	for i in range(first_point, last_point):
		child[i] = parent1[i]
	pointer_child = last_point % 8

	# copy numbers from the second parent to the child, 
	# that are not from the first parent,
	# starting at the cut off point of the copied first parent
	for i in range(0, 8):
		pointer_p2 = (i + last_point) % 8
		if parent2[pointer_p2] not in child:
			child[pointer_child] = parent2[pointer_p2]
			pointer_child = (pointer_child + 1) % 8
	return child
