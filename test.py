from nav import Point, Map

def getInput():
	n_points = 500#int(input("No of points : ")) # 400
	length = 10#int(input("Enter length : ")) # 10
	width = 8#int(input("Enter width : ")) # 8

	m_map = Map()
	t_start = m_map.defineStart()
	m_map.bakePath(n_points, length, width)
	# m_map.showAllConnections(m_map)
	# m_map.showStart(m_map)

	start = m_map.findStart(t_start) # Index of starting point
	dest = 0 # Index of destination point

	path = m_map.getPath(start, dest)
	m_map.showPath(path)


getInput()
