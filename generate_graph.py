import random

def gen_graph(num_vertices):
	filename = "test2"#str(num_vertices)
	f = open(filename + ".in", "w")
	f.write(filename + "\n")
	for i in range(num_vertices-1):
		for j in range(i+1, num_vertices):
			val = random.randint(1, 99)
			string = str(i) + " " + str(j) + " " + str(val)
			if i != num_vertices-2:
				string += "\n"
			f.write(string)
	f.close()

if __name__ == '__main__':
	#gen_graph(25)
	#gen_graph(50)
	#gen_graph(100)
	gen_graph(4)