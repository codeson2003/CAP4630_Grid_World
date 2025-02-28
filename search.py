import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation

from utils import *
from grid import *
from search_algorithms import bfs, dfs, gbfs

def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons

if __name__ == "__main__":
    epolygons = gen_polygons('TestingGrid/world1_enclosures.txt')
    tpolygons = gen_polygons('TestingGrid/world1_turfs.txt')

    source = Point(8,10)
    dest = Point(43,45)

    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point
    
    # Draw enclosure polygons
    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])
    
    # Draw turf polygons
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])

    #### Here call your search to compute and collect res_path
    print("1. DFS\n2. BFS\n3. GBFS\n4. A*\n", end = '')
    user_input = input("Choose a search algorithm to run (enter number 1-4): ")
    choice = int(user_input)

    #switch to choose which algorithm you'd like to run
    match choice:
        case 1:
            res_path, path_cost, nodes_expanded = dfs(source,dest,epolygons)
        case 2:
            res_path, path_cost, nodes_expanded = bfs(source,dest,epolygons)
        case 3:
            res_path, path_cost, nodes_expanded = gbfs(source,dest,epolygons,tpolygons)
        case _:
            print("Error: Please enter a number between 1 and 4. ")
            exit(1)

    
    
    for i in range(len(res_path)-1):
        draw_result_line(ax, [res_path[i].x, res_path[i+1].x], [res_path[i].y, res_path[i+1].y])
        plt.pause(0.1)
    print(nodes_expanded, " ", path_cost)
    plt.show()
