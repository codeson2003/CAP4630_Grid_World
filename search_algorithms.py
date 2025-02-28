from matplotlib.path import Path
import math
from utils import *
from grid import Point


"""
    function BEST-FIRST-SEARCH(problem, f) returns a solution or failure
        node <- NODE(STATE=problem.INITIAL)
        frontier <- a priority queue ordered by f, with node as an element
        reached <- a lookup table, with one entry with key problem.INITIAL and value node
        while not IS-EMPTY(frontier) do
            node <- POP(frontier)
            if problem.IS-GOAL(node.STATE) then return node
            for each child in EXPAND(problem, node) do
                s <- child.STATE
                if s is not in reached or child.PATH-COST < reached[s].PATH-COST then
                    reached[s] <- child
                    add child to frontier
return failure
"""
def gbfs(source,dest,epolygons,tpolygons):

    nodes_expanded = 0
    node = {'state': source, 'parent': None}
    frontier = PriorityQueue()
    frontier.push(node, hueristic(source, dest))
    reached = {source: node}

    while not frontier.isEmpty():
        node = frontier.pop()
        current = node['state']

        if current == dest:
            path = []
            current_node = node
            while current_node is not None:
                path.append(current_node['state'])
                current_node = current_node['parent']
            path.reverse()
            path_cost = sum(action_cost(path[i+1], tpolygons) for i in range(len(path) - 1))
            return path, path_cost, nodes_expanded
        
        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x,y = current.x + dx, current.y + dy
            if 0 <= x < 50 and 0 <= y < 50:
                successor = Point(x,y)

                if not any(enclosure_check(successor, ep) for ep in epolygons):
                    child = {'state': successor, 'parent': node}
                    s = successor
                    if s not in reached :
                        reached[s] = child
                        nodes_expanded+=1
                        frontier.push(child, hueristic(s, dest))
    return None, None, nodes_expanded


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
        current = node['state']
        if current == dest:
            path = []
            current_node = node
            while current_node is not None:
                path.append(current_node['state'])
                current_node = current_node['parent']
            path.reverse()
            return path, len(path) - 1, nodes_expanded
        
        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x,y = current.x + dx, current.y + dy
            if 0 <= x < 50 and 0 <= y < 50:
                successor = Point(x,y)

                if not any(enclosure_check(successor, ep) for ep in epolygons):
                    child = {'state': successor, 'parent': node}
                    s = successor

                    if s not in reached:
                        reached.add(s)
                        frontier.push(child)
                        nodes_expanded+=1


    return None, None, nodes_expanded



"""
node <- NODE(problem.INITIAL)
if problem.IS-GOAL(node.STATE) then return node
frontier <- a FIFO queue, with node as an element
reached <- {problem.INITIAL}
while not IS-EMPTY(frontier) do:
    node <- POP(frontier)
    for each child in EXPAND(problem, node) do:
        s <- child.STATE
        if problem.IS-GOAL(s) then return child
        if s is not in reached then:
            add s to reached
            add child to frontier
return failure
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

"""
    Action cost algorithm to determine cost of next move!
    Parameters: point - point in question, tpolygons - turf polygons

    Returns 1.5 if inside or on edge of turf polygon, else 1
"""
def action_cost(point, tpolygons):

    if any(enclosure_check(point, tp) for tp in tpolygons):
        return 1.5

    return 1

"""
    SLD hueristic function to calculate the straight line distance between the source and destination
    uses euclidean distance for the calculation
    
"""
def hueristic(point,dest):

    return math.sqrt((point.x - dest.x) ** 2 + (point.y - dest.y) ** 2)
