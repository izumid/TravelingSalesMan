import math


class City:
	def __init__(self, name, latitude, longitude):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude


def get_distance(city1, city2):
	# Calcula a distância euclidiana entre duas cidades usando as coordenadas de latitude e longitude
	lat1, lon1 = math.radians(city1.latitude), math.radians(city1.longitude)
	lat2, lon2 = math.radians(city2.latitude), math.radians(city2.longitude)
	dlat = lat2 - lat1
	dlon = lon2 - lon1
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	radius = 6371  # raio médio da Terra em quilômetros
	distance = radius * c
	return distance


def tsp_nearest_neighbor(cities):
	num_cities = len(cities)
	visited = [False] * num_cities
	path = [0] * num_cities  # Inicia o caminho com a cidade de índice 0
	visited[0] = True
	total_distance = 0
	nearest_distance_value = []

	for i in range(num_cities - 1):
		current_city = path[i]
		nearest_neighbor = None
		nearest_distance = float('inf')
		
		for j in range(num_cities):
			if not visited[j] and j != current_city:
				distance = get_distance(cities[current_city], cities[j])
				if distance < nearest_distance:
					nearest_distance = distance
					nearest_neighbor = j
				
		path[i + 1] = nearest_neighbor
		visited[nearest_neighbor] = True
		nearest_distance_value.append(nearest_distance)
		total_distance += nearest_distance

	# Volta para a cidade inicial
	nearest_distance_value.append(get_distance(cities[path[-1]], cities[0]))
	total_distance += get_distance(cities[path[-1]], cities[0])
	path.append(0)
	return path, total_distance, nearest_distance_value


def mst_prim(cities):
	num_cities = len(cities)
	visited = [False] * num_cities
	key = [float('inf')] * num_cities
	parent = [None] * num_cities

	# Define a primeira cidade como raiz da árvore
	key[0] = 0

	for _ in range(num_cities):
		min_key = float('inf')
		min_index = None
		for i in range(num_cities):
			if not visited[i] and key[i] < min_key:
				min_key = key[i]
				min_index = i

		visited[min_index] = True

		for j in range(num_cities):
			if not visited[j]:
				distance = get_distance(cities[min_index], cities[j])
				if distance < key[j]:
					key[j] = distance
					parent[j] = min_index

	# Constrói a árvore geradora mínima
	mst = []
	total_distance = 0
	for i in range(1, num_cities):
		mst.append((parent[i], i))
		total_distance += get_distance(cities[parent[i]], cities[i])

	return mst, total_distance


def print_path(cities, path, nearest_distance_value):
	for i in range(len(path) - 1):
		city1 = cities[path[i]]
		city2 = cities[path[i + 1]]
		distance = nearest_distance_value[i]
		print(f"  {city1.name} -> {city2.name}; distância: {distance:.2f};")


def print_mst(cities, mst,adjacency_matrix):
	for x in range(len(mst)):
		for z in mst: 
			if z[0] == x: print(f"  {cities[z[0]].name} -> {cities[z[1]].name}; distância: { adjacency_matrix[z[0]][z[1]]:.2f};")


def main():
	cities = [
		City("Americana", -22.7426, -47.3367),
		City("Botucatu", -22.8884, -48.4413),
		City("Cósmopolis", -22.652, -47.1986),
		City("Descavado", -21.9099, -47.6216),
		City("Embu das Artes", -23.6546, -46.8594),
		City("Franco da Rocha", -23.3385, -46.7386),
		City("Guarulhos", -23.4758, -46.5257),
		City("Hortolândia", -22.8698, -47.2220),
		City("Itupeva", -23.1631, -47.0599),
		City("Jundiai", -23.1972, -46.8787),
		City("Vargem grande do sol", -21.8188, -46.8856),
		City("Mauá", -23.6678, -46.4607)
	]

	num_cities = len(cities)
	adjacency_matrix = [[0] * num_cities for _ in range(num_cities)]
	for i in range(num_cities):
		for j in range(i + 1, num_cities):
			distance = get_distance(cities[i], cities[j])
			adjacency_matrix[i][j] = distance
			adjacency_matrix[j][i] = distance

	print("| ---------- TSP - Vizinhos mais próximos ---------- |")
	path, total_distance,nearest_distance_value = tsp_nearest_neighbor(cities)
	print(f"| ---------- Custo total: {total_distance:.2f}Km ----------------- |")
	print("\nMelhor caminho:")
	print_path(cities, path,nearest_distance_value)

	print("\n\n| ---------- Algoritmo de Árvore Geradora Mínima --- |")
	mst, total_distance = mst_prim(cities)
	print(f"| ---------- Custo total: {total_distance:.2f}Km ----------------- |")
	print_mst(cities, mst, adjacency_matrix)


if __name__ == '__main__':
	main()