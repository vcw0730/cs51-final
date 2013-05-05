from tsp_genetic import *
from tsp_dynamic import *
from greedy import *
from PIL import Image, ImageDraw, ImageFont
import time, os, ast

#solution[0] = greedy, solution[1] = genetic, solution[2] = dynamic
solution = [[],[],[]]


def generate_graph(num):
    """ instantiate graph and locations """
    g = Graph(num)
    locs = copy.copy(g.points)

    # remove start city
    start_end = locs.pop()

    # error checking
    assert(len(locs) == num - 1)
    assert(start_end not in locs)

    return g, locs, start_end

def update(ourset, num, n):
    """ updates our set (solution/distance/time) depending on algorithm """
    if num == 0:
        ourset[0] = n
    elif num == 1:
        ourset[1] = n
    elif num == 2:
        ourset[2] = n
    else:
        print "Error: num is not in range!"
    return ourset

def clear():
    """ use to clear solution_set or distance_set """
    return [[], [], []]

def percent_error(d1, d2):
    return round(((abs(d1 - d2) / d2) * 100), 2)

def scale_distance(d1, d2, line_len):
    larger = max(d1, d2)

    len_d1 = (d1 * (line_len/larger))
    len_d2 = (d2 * (line_len/larger))
    return (len_d1, len_d2)


def print_path(num, solution_set, distance_set, start_end, cities, d, t):
    assert (num < 3 and num > -1)
    create_png(num, solution_set, distance_set, start_end, cities, d, t)
    print "Current path for traveling between these", cities, "cities is: "
    print " 1 ) ", start_end
    sol = solution_set[num]
    for i in range(len(sol)):
        print "", i + 2, ") ", sol[i]
    print "", len(sol) + 2, ") ", start_end
    print "Total distance traveled:", distance_set[num]
    return

def create_png(num, solution_set, distance_set, start_end, cities, d, t):
    path = solution_set[num]
    city = start_end
    path.append(start_end)
    path_length = len(path)
    
    size = (500,500)
    padding = (50,50)
    im = Image.new("RGB",size,(255,255,255))

    draw = ImageDraw.Draw(im)
    font = ImageFont.load_default()

    s = 4 #scale
    p = 50 #padding, shift map over to middle of image
    tp = 15 + p #shift over text padding a bit to account for vertices later        
    low_bound = 90
    color = (255 - low_bound) / (path_length - 1) # use to change colors

    #draw edges
    for i in range(path_length - 1):
        c1 = path[i]
        c2 = path[i + 1]

        draw.line((s*c1[0]+p, s*c1[1]+p, s*c2[0]+p, s*c2[1]+p), fill = (0,0,0))
        #label each city with coordinates
        draw.text((s*c1[0]+tp, s*c1[1]+p), str(c1), font=font, fill = (0,0,i*color+low_bound))

    c1 = path[path_length-1] #this is the starting city due to the way append works
    c2 = path[0]
    draw.line((s*c1[0]+p, s*c1[1]+p, s*c2[0]+p, s*c2[1]+p), fill = (0,0,0))
    draw.text((s*c1[0]+tp, s*c1[1]+p), str(c1), font=font, fill = (255,0,0))
    
    #draw vertices (that aren't the starting/ending)
    path.remove(city)
    for i in range(len(path)):
        pos = path[i]
        x = s*pos[0] + p
        y = s*pos[1] + p
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 0, 0),
                     fill = ((0, 0, (i*color+low_bound))))

    #draw starting/ending city with RED
    x = s*city[0] + p
    y = s*city[1] + p
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), outline = (0, 0, 0), fill = (255,0,0))

    d1, d2 = scale_distance(distance_set[num], d, 170)
    error = percent_error(d1, d2)

    draw.line([(280,20), (300 + d1, 20)], fill = (255, 0, 0), width = 5)
    draw.line([(280,30), (300 + d2, 30)], fill = (0, 0, 255), width = 5)

    draw.text((10,20), "Distance: " + str(distance_set[num]), font=font, fill = (0,0,0))
    draw.text((10,30), "Baseline distance: " + str(d), font=font, fill = (0,0,0))
    draw.text((10,40), "Percent error: " + str(error) + "%", font=font, fill = (0,0,0))
    if num == 0:
        name = "greedy"
    elif num == 1:
        name = "genetic"
    else:
        name = "dynamic"
    filename = "tsp_" + name + ".png"
    draw.text((10,10), "Algorithm used: " + name + ", time: " + str(t) + " seconds", font=font, fill = (0,0,0))

    del draw
    im.save(filename, "PNG")

    os.system(filename)
    
    print ".png drawn!"


