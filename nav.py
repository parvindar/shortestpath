from random import uniform, randint
import matplotlib.pyplot as plt
import numpy as np
from heapq import heapify, heappush, heappop
# from APQ import APQ


class Point:
	x, y, connections = None, None, set()

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.connections = set()

	def __str__(self):
		return '('+str(round(self.x, 2))+','+str(round(self.y, 2))+')'

	def distance(self, point):
		return ((self.x-point.x)**2 + (self.y-point.y)**2)**0.5

	def isValid(self, point, max_distance):
		return self.distance(point)<max_distance and self.distance(point)>0



class Map:

	# Define Variables
	points = []
	start = []


	# Define Starting Point
	def defineStart(self):
		# x, y = input("Enter x : "), input("Enter y : ")
		x, y = 1, 2
		self.start = Point(float(x), float(y))
		return self.start


	# Build the points and the paths between them
	def bakePath(self, n, l, w):
		# n = no of points
		# l = length, w = width

		# Build Points
		for x in range(n):
			self.points.append(Point(uniform(0, l), uniform(0, w)))

		# Build Connections for each point
		for i in range(n):
			n_connections = randint(0, int(n/2))
			if i%100==0:
				print("processing " + str(i+1) + "th point")

			for j in range(n_connections):
				toAppend = randint(0, n-1)
				if (self.points[i].isValid(self.points[toAppend], 0.7)):
					self.points[i].connections.add(toAppend)
					# choose = uniform(0, 1)
					# if choose>0.5 or True:
					self.points[toAppend].connections.add(i) # Comment later

		for i in range(n):
			self.points[i].connections = list(self.points[i].connections)


	# Show the whole roadmap with all the connections
	def showAllConnections(self):
		pts_x = [pt.x for pt in self.points]
		pts_y = [pt.y for pt in self.points]
		plt.scatter(pts_x, pts_y)
		n = len(self.points)
		for i in range(n):
			for j in range(len(self.points[i].connections)):
				xs = [self.points[i].x, self.points[self.points[i].connections[j]].x]
				ys = [self.points[i].y, self.points[self.points[i].connections[j]].y]
				plt.plot(xs, ys, c='g')
		plt.show()


	# Show Start with nearest neighbours
	def showStart(self):
		dist = 1000000
		for x in self.points:
			if(self.start.distance(x)<dist):
				nearest = x
				dist = self.start.distance(x)
		plt.scatter(self.start.x, self.start.y, c='r', zorder=2)
		pts_x = [pt.x for pt in self.points]
		pts_y = [pt.y for pt in self.points]
		plt.scatter(pts_x, pts_y)
		n = len(self.points)
		for i in range(n):
			for j in range(len(self.points[i].connections)):
				xs = [self.points[i].x, self.points[self.points[i].connections[j]].x]
				ys = [self.points[i].y, self.points[self.points[i].connections[j]].y]
				plt.plot(xs, ys, c='g', zorder=1)
		plt.plot([self.start.x, nearest.x], [self.start.y, nearest.y], c='r', zorder=2)
		dest = self.points[0]
		plt.scatter(dest.x, dest.y, c='y', zorder=2)
		plt.show()


	# Show Start with nearest neighbours
	def showPath(self, path):
		# plt.figure(figsize=(20, 20), facecolor='w', edgecolor='k')
		dist = 1000000
		for x in self.points:
			if(self.start.distance(x)<dist):
				nearest = x
				dist = self.start.distance(x)
		n = len(self.points)
		for i in range(n):
			for j in range(len(self.points[i].connections)):
				xs = [self.points[i].x, self.points[self.points[i].connections[j]].x]
				ys = [self.points[i].y, self.points[self.points[i].connections[j]].y]
				plt.plot(xs, ys, c='lightgray', zorder=1)
		plt.plot([self.start.x, nearest.x], [self.start.y, nearest.y], c='y', zorder=2)
		dest = self.points[0]

		pts_x = [pt.x for pt in self.points]
		pts_y = [pt.y for pt in self.points]
		plt.scatter(pts_x, pts_y, c='grey', zorder=1.2, s=10)

		# Show Path
		xs = [self.points[pt].x for pt in path]
		ys = [self.points[pt].y for pt in path]
		plt.plot(xs, ys, c='b', zorder=2)
		plt.scatter(self.start.x, self.start.y, c='y', zorder=2)
		plt.scatter(dest.x, dest.y, c='r', zorder=2)

		plt.show()


	# Find starting point in saved points
	def findStart(self, start):
		dist = 1000000
		for i, x in enumerate(self.points):
			if(self.start.distance(x)<dist):
				nearest = i
				dist = self.start.distance(x)
		return nearest



	# Print Path
	# def printPath(self, path):
	# 	for i in path:
	# 		print('(' + str(self.points[i].x) + ', ' + str(self.points[i].y)+  ')')

	# Get Path from current position
	def getPath(self, start, dest):

		path = []
		points = self.points
		starting, destination = self.points[start], self.points[dest]
		print("start:"+str(start))
		print("starting : " + str(starting))

		# each element of all paths is stored as below
		# d = distance_covered_till_now
		# d1 = distance from destination
		# [
		# 	d+d1,
		# 	d,
		# 	index_of_current_position,
		# 	coming_from_index
		# ]
		all_paths = [[starting.distance(destination), 0, start, -1]]
		dist = 100000
		coming_from_relations = {}

		# visited = [False for i in range(len(points))]
		# orders = [0 for i in range(len(points))]
		# curr_order = 1

		visited = set()

		while len(all_paths):
			curr = all_paths[0]
			heappop(all_paths)
			curr_index, dist_covered_till_now = curr[2], curr[1]

			if curr_index in visited:
				print("=======================already visited===========||||||||||||||||||||||||||")
				
			visited.add(curr_index)
			print("curr_index:"+str(curr_index)+"  printing connections for " + str(points[curr_index])+' : '  + str([str(points[con]) for con in points[curr_index].connections]))

			for i, conn in enumerate(points[curr_index].connections):
				print("conn : " + str(self.points[conn]))
				if conn==dest:
					coming_from_relations[conn] = curr_index
					print(coming_from_relations)
					path.append(conn)
					while(conn in coming_from_relations) and conn!=start:
						print("conn : " + str(conn) + '--' + str(points[conn]))
						path.append(coming_from_relations[conn])
						conn = coming_from_relations[conn]
					for i in path:
						print(self.points[i])
					return path

				d = points[curr_index].distance(points[conn])+dist_covered_till_now
				d1 = destination.distance(points[conn])

				# If it's a loop , do nothing
				# if (curr_index in coming_from_relations):# and (coming_from_relations[curr_index]==conn):
				# 	temp_curr_index = curr_index
				# 	changed = False
				# 	while(temp_curr_index in coming_from_relations):
				# 		temp_curr_index = coming_from_relations[temp_curr_index]
				# 		if temp_curr_index==conn:
				# 			changed = True
				# 			break
				# 	if changed:
				# 		continue
				# coming_from_relations[conn] = curr_index
				print("indexed")

				try:
					# if conn in coming_from_relations:
					index = list(np.array(all_paths)[:, 2]).index(conn)
					if(d<all_paths[index][1]):
						print("found a shorter way!\n")
						all_paths[index][1] = d
						all_paths[index][0] = d+d1
						all_paths[index][3] = curr_index
						heapify(all_paths)
						coming_from_relations[conn] = curr_index
							# print(coming_from_relations)

							# If it's a loop , do nothing
							# if (curr_index in coming_from_relations):# and (coming_from_relations[curr_index]==conn):
							# 	temp_curr_index = curr_index
							# 	changed = False
							# 	while(temp_curr_index in coming_from_relations):
							# 		temp_curr_index = coming_from_relations[temp_curr_index]
							# 		if temp_curr_index==conn:
							# 			changed = True
							# 			break
							# 	if changed:
							# 		continue
							# 	else:
							# 		coming_from_relations[conn] = curr_index
							# else:
							# 	coming_from_relations[conn] = curr_index
					# else:
					# 	raise ValueError() # This will give valueerror and will go into except

				except (IndexError, ValueError):
					if conn in coming_from_relations:
						print("It has already been popped out, SORRY !! Moving ahead!!")
						continue
					print("push")
					heappush(all_paths, [d+d1, d, conn, curr_index])
					coming_from_relations[conn] = curr_index
					# print(coming_from_relations)

					# # If it's a loop , do nothing
					# if (curr_index in coming_from_relations):# and (coming_from_relations[curr_index]==conn):
					# 	temp_curr_index = curr_index
					# 	changed = False
					# 	while(temp_curr_index in coming_from_relations):
					# 		temp_curr_index = coming_from_relations[temp_curr_index]
					# 		if temp_curr_index==conn:
					# 			changed = True
					# 			break
					# 	if changed:
					# 		continue
					# 	else:
					# 		coming_from_relations[conn] = curr_index
					# else:
					# 	coming_from_relations[conn] = curr_index


					# if (curr_index in coming_from_relations) and (coming_from_relations[curr_index]==conn):
					# 	continue
					# else:
					# 	coming_from_relations[conn] = curr_index

			# visited[curr_index] = True
			print("\n\n")

		# for i in path:
		# 	print('(' + str(self.points[i].x) + ', ' + str(self.points[i].y)+  ')')


		# for conn in starting.connections:
			# d = starting.distance(points[conn])
			# d1 = destination.distance(points[conn])
			# if d+d1<dist:
			# 	dist = d+d1
			# 	all_paths.append([conn, ])
			# 	heapify(all_paths)
