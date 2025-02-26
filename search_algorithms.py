from matplotlib.path import Path

from utils import *
from grid import Point






"""
    function DEPTH-FIRST-SEARCH(problem) returns a solution node or failure
    frontier <- a LIFO queue (stack) with NODE(problem.INITIAL) as an element
        while not IS-EMPTY(frontier) do
            node <- POP(frontier)
            if problem.IS-GOAL(node.STATE) then return node
            for each child in EXPAND(problem, node) do
                if not IS-CYCLE(child) do
                    add child to frontier
    return result

"""
def dfs(source, dest, epolygons):
    
    nodes_expanded = 0

    node = {'state': source, 'parent': None}
    
    frontier = Stack()
    frontier.push(node)
    reached = {source}

    while not frontier.isEmpty():
        node = frontier.pop()
        if node['state'] == dest:
            return [node['state']], 0, nodes_expanded
        
        current = node['state']

        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x,y = current.x + dx, current.y + dy
            if 0 <= x < 50 and 0 <= y < 50:
                successor = Point(x,y)

                if not any(enclosure_check(successor, ep) for ep in epolygons):
                    child = {'state': successor, 'parent': node}
                    s = successor

                    if s not in reached:
                        reached.add(s)
                        

    return None, None, nodes_expanded



"""
BFS Pseudocode (Breadth-First Search) from class:
- node <- NODE(problem.INITIAL)                     # Create a node with the initial state
- if problem.IS-GOAL(node.STATE) then return node   # Check if initial state is the goal, return if true
- frontier <- a FIFO queue, with node as an element # Initialize a FIFO (First-In, First-Out) queue with the initial node
- reached <- {problem.INITIAL}                      # Track reached states to avoid cycles, start with initial state
- while not IS-EMPTY(frontier) do:                  # Continue while there are nodes to explore
    - node <- POP(frontier)                         # Remove and get the next node from the queue
    - for each child in EXPAND(problem, node) do:   # Generate all possible child states from the current node
        - s <- child.STATE                          # Get the state of the child
        - if problem.IS-GOAL(s) then return child   # If the child's state is the goal, return the child node
        - if s is not in reached then:              # If we haven't seen this state before
            - add s to reached                      # Mark the state as reached
            - add child to frontier                 # Add the child node to the queue for exploration
- return failure                                    # No path found, return failure
"""
def bfs(source, dest, epolygons):

    nodes_expanded = 0

    node = {'state': source, 'parent': None}
    if node['state'] == dest:
        return [node['state']], 0, nodes_expanded
    
    frontier = Queue()
    frontier.push(node)
    reached = {source}

    while not frontier.isEmpty():
        node = frontier.pop()
        current = node['state']
        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x,y = current.x + dx, current.y + dy
            if 0 <= x < 50 and 0 <= y < 50:
                successor = Point(x,y)
                
                if not any(enclosure_check(successor, ep) for ep in epolygons):
                    child = {'state': successor, 'parent': node}
                    s = successor

                    if s == dest:
                        path = []
                        current_node = child
                        while current_node is not None:
                            path.append(current_node['state'])
                            current_node = current_node['parent']
                        path.reverse()
                        return path, len(path) - 1, nodes_expanded
                    
                    if s not in reached:
                        reached.add(s)
                        frontier.push(child)
                        nodes_expanded += 1

    return None, None, nodes_expanded

"""
    Supporting method to detemine if a point lies within or on the edge of an enclosure.
    (ray casting algorithm)

    point: the point in question.
    polygon: the polygon in question.

    returns true if point lies within or on polygon, false otherwise. 
"""
def enclosure_check(point, polygon):
    
    #turning the polygon into a set of points
    poly_points = [(pt.x, pt.y) for pt in polygon]

    #edge case to check if the point lies on an edge
    if is_on_edge(poly_points, point):
        return True
    

    count = 0
    xp, yp = point.x, point.y

    #calculating the edges
    edges = []
    for i in range(len(poly_points)):
        p1 = poly_points[i]
        p2 = poly_points[(i+1) % len(poly_points)] #modulo used to connect last point to first point to close poly
        edges.append((p1,p2))
    
    #calculating count of
    for edge in edges:
        (x1,y1), (x2,y2) = edge
        if (yp<y1) != (yp<y2) and xp < x1 + ((yp-y1) / (y2-y1)) * (x2-x1):
            count+=1

    return count % 2 == 1


"""
    Supporting method to the enclosure_check() algo,
    checks if a point is on the edge of a polygon
"""
def is_on_edge(poly_points, point):

    px,py = point.x, point.y

    for i in range(len(poly_points)):
        p1 = poly_points[i]
        p2 = poly_points[(i + 1) % len(poly_points)]

        x1, y1 = p1
        x2, y2 = p2

        #checks if the px or py is between the min,max of x1,x2 , y1,y2 respectively
        if(min(x1, x2) <= px <= max(x1,x2) and min(y1,y2) <= py <= max(y1,y2)):
            cross_product = ((y2-y1) * (px - x1) - (x2-x1) * (py - y1))
            if abs(cross_product) < 0.0001:
                return True
            
    return False

