from matplotlib.path import Path

from utils import Queue
from grid import Point



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

    point: the point in question.
    polygon: the polygon in question.

    returns true if point lies within or on polygon, false otherwise. 
"""
def enclosure_check(point, polygon):
    
    #turning the polygon into a set of points and then turning those points into a path
    poly_points = [(pt.x, pt.y) for pt in polygon]
    path = Path(poly_points)

    #now check if our point lies on that path
    point_convert = (point.x, point.y)
    return path.contains_point(point_convert)

