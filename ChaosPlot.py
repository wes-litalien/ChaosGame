# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 09:12:13 2022

@author: wlitalien
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import random
from shapely.geometry import Polygon, Point

def get_random_point_in_polygon(poly):
    #https://gis.stackexchange.com/questions/6412/generate-points-that-lie-inside-polygon
     minx, miny, maxx, maxy = poly.bounds
     while True:
         p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
         if poly.contains(p):
             return p

R = 1 #enclosing circle Radius
n = 4 #verticies of polygon
phi = (1 + math.sqrt(5))/2 # https://en.wikipedia.org/wiki/Chaos_game
fractional_distance = 1/2
restrict_verticies = True

vertex_points_x, vertex_points_y = [], []

vertex_angle = 2*math.pi/n # angle between verticies
theta_0 = 3*math.pi/2 + vertex_angle/2

for v in range(1, n+1):
    vertex_points_x.append(R*math.cos(theta_0 + (v-1)*vertex_angle))
    vertex_points_y.append(R*math.sin(theta_0 + (v-1)*vertex_angle)) # Bottom right corner, 270 + half angle

points_x = vertex_points_x.copy()
points_y = vertex_points_y.copy()

vertex_points = []
for i in range(n):
    vertex_points.append(tuple([vertex_points_x[i], vertex_points_y[i]]))
    
mypoly = Polygon(vertex_points)
first_point = get_random_point_in_polygon(mypoly)

points_x.append(first_point.x)
points_y.append(first_point.y)

fig = plt.figure(figsize=(14,14))
ax = plt.axes(xlim=(min(vertex_points_x),max(vertex_points_x)),ylim=(min(vertex_points_y),max(vertex_points_y)))
scatter = ax.scatter(points_x, points_y, color='k', s=1)

current_point_x = first_point.x
current_point_y = first_point.y

plt.draw()

previous_index = n

for i in range(25000):
    if not i % 100:
        print(i)
        
    if restrict_verticies:
        random_point_index = vertex_points_x.index(random.choice(vertex_points_x))
        while previous_index == random_point_index:
            #cant be the same vertex twice
            random_point_index = vertex_points_x.index(random.choice(vertex_points_x))
    else:
        random_point_index = vertex_points_x.index(random.choice(vertex_points_x))
        
    previous_index = random_point_index
    random_point_x = vertex_points_x[random_point_index]
    random_point_y = vertex_points_y[random_point_index]
    
    current_point_x = (random_point_x - current_point_x)*fractional_distance + current_point_x
    current_point_y = (random_point_y - current_point_y)*fractional_distance + current_point_y
    
    points_x.append(current_point_x)
    points_y.append(current_point_y)
    
    scatter.set_offsets(np.c_[points_x, points_y])
    fig.canvas.draw_idle()
    plt.pause(0.01)
    

plt.waitforbuttonpress()