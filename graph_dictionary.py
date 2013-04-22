import random 
import math
   
class Graph(object):
  """
  Graph representation for a Traveling Salesman Problem:
  We will use a Dictionary to represent an undirected weighted graph using
  a key-value pair: the key will be a city, and the value will be another
  dictionary with keys representing a connected city and the values are their
  corresponding distances.
  """
   
  # points is the number of points we want to generate
  # if lst != 0, then we are inputting a list
  def __init__(self, number):
    self.points = self.generate_points(number)
    self.graph = self.generate_complete_graph()
     
  # generate_point generates a random point in the area
  # bounded by a square of side 100 that's not already in lst
  # returns the point
  def generate_point (self, lst):
    a = (random.randint(0, 100), random.randint(0, 100))
    while a in lst:
      a = (random.randint(0, 100), random.randint(0, 100))
    return a
 
  # generates a lst of (number) points (x, y) in the cartesian plane
  # returns the lst
  def generate_points (self, number):
    lst = []
    for each in range(number):
      a = self.generate_point(lst)
      lst.append(a)
    return lst
 
  # udpates the edges in the dictionary
  def update_edge(self, point1, point2):
    dist = self.distance(point1, point2)
    self.graph[point1].update({point2: dist})
    self.graph[point2].update({point1: dist})
     
  # returns distance between two points
  def distance (self, point1, point2):
    return round (math.sqrt( (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2), 3)
     
   
  # generates a complete graph
  def generate_complete_graph(self):
    result = {}
    length = len(self.points)
    for i in range(length):
      point1 = self.points[i]
      # prevents repeating edges like (A, B) and (B,A)
      for j in range(i+1, length):
        point2 = self.points[j]
        dist = self.distance(point1, point2)
        keys = result.keys()
        if point1 in keys and point2 in keys:
            result[point1].update({point2: dist})
            result[point2].update({point1: dist})
        elif point1 in keys and point2 not in keys:
            result[point1].update({point2: dist})
            result[point2] = {point1: dist}
        elif point2 in keys and point1 not in keys:
            result[point2].update({point1: dist})
            result[point1] = {point2: dist}
        else:
            result[point1] = {point2: dist}
            result[point2] = {point1: dist}
    return result