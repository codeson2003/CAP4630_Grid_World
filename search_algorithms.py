# search_algorithms.py
from utils import Queue
from grid import Point

def bfs(source, dest, epolygons):
    """Breadth-First Search: returns path, path_cost, nodes_expanded.
    
    Args:
        source (Point): Starting point (problem.INITIAL).
        dest (Point): Destination point (goal state).
        epolygons (list): List of enclosure polygons (list of Point objects).
    
    Returns:
        tuple: (path, path_cost, nodes_expanded) where path is a list of Points,
               path_cost is the number of steps, and nodes_expanded is the count of expanded nodes.
    """
    # node <- NODE(problem.INITIAL)
    node = {'state': source, 'parent': None}
    
    # if problem.IS-GOAL(node.STATE) then return node
    if source == dest:
        return [source], 0, 0  # Path with just the source, cost 0, no nodes expanded
    
    # frontier <- a FIFO queue, with node as an element
    frontier = Queue()
    frontier.push(node)
    
    # reached <- {problem.INITIAL}
    reached = {source}  # Set of states (points) we've reached
    
    # Count nodes expanded (when we first explore a node)
    nodes_expanded = 0
    
    # while not IS-EMPTY(frontier) do
    while not frontier.isEmpty():
        # node <- POP(frontier)
        node = frontier.pop()
        current_state = node['state']
        
        # for each child in EXPAND(problem, node) do
        for successor in get_successors(current_state, epolygons):  # EXPAND generates child states
            child = {'state': successor, 'parent': node}
            s = successor  # s <- child.STATE
            
            # if problem.IS-GOAL(s) then return child
            if s == dest:
                # Reconstruct path from child to source
                path = []
                current = child
                while current is not None:
                    path.append(current['state'])
                    current = current['parent']
                path.reverse()
                return path, len(path) - 1, nodes_expanded
            
            # if s is not in reached then
            if s not in reached:
                # add s to reached
                reached.add(s)
                # add child to frontier
                frontier.push(child)
                nodes_expanded += 1  # Increment nodes expanded when adding to frontier (first time reaching)
    
    # return failure
    return None, None, nodes_expanded

# Helper function (remains the same)
def get_successors(point, epolygons):
    """Get valid successor points (up, right, down, left) avoiding enclosures."""
    successors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Order: up, right, down, left
        nx, ny = point.x + dx, point.y + dy
        if 0 <= nx < 50 and 0 <= ny < 50:  # Check grid boundaries
            successor = Point(nx, ny)
            # Check if successor is not inside or on edge of any enclosure
            if not any(is_inside_or_on_edge(successor, ep) for ep in epolygons):
                successors.append(successor)
    return successors

# Helper function (remains the same)
def is_inside_or_on_edge(point, polygon):
    """Check if a point is inside or on the edge of a polygon."""
    from matplotlib.path import Path
    path = Path([p.to_tuple() for p in polygon])
    return path.contains_point(point.to_tuple())