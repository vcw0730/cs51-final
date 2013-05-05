from tsp_genetic import *
from tsp_dynamic import *
from greedy import *
from PIL import Image, ImageDraw, ImageFont
import time, os, ast

#solution[0] = greedy, solution[1] = genetic, solution[2] = dynamic
solution = [[],[],[]]

def update_solution(num, newsol):
    """ updates our solution depending on algorithm """
    global solution
    if num == 0:
        solution[0] = newsol
    elif num == 1:
        solution[1] = newsol
    elif num == 2:
        solution[2] = newsol
    else:
        print "Error: num is not in range!"
    return

def clear_solution():
    for i in range(3):
        update_solution(i, [])
        update_dist(i, None)

def update_cities(n):
    while n < 2:
        n = int(raw_input("Please enter a number greater than 1! "))
    cities = n
    return

def update_graph(n):
    a = Graph(n)
    return

def update_locs(lst):
    locs = lst
    return

def update_start_end(city):
    start_end = city
    return

def update_dist(num, n):
    if num == 0:
        dist[0] = n
    elif num == 1:
        dist[1] = n
    elif num == 2:
        dist[2] = n
    else:
        print "Error: num is not in range!"
    return

def get_solution(num):
    assert num < 3 and num > -1
    return solution[num]

def get_cities():
    global cities
    return cities

def get_graph():
    global a
    return a

def get_locs():
    global locs
    return locs

def get_start_end():
    global start_end
    return start_end

def get_dist(num):
    global dist
    assert num < 3 and num > -1
    return dist[num]

def reorder_sol(num, sol, initial):
    """ given a solution and an initial city, reorders list so that
        initial city is at the front but otherwise unchanged
        except it returns all the cities *after* initial """
    assert initial in sol
    x = sol.index(initial)
    newsol = sol[x+1:] + sol[:x]
    return newsol

def change_graph(y):
    # generate new graph to run on, update all values accordingly
    update_cities(y)
    update_graph(y)
    a = get_graph()
    locs = a.points
    start_end = locs[0]
    locs.remove(start_end)

    update_locs(locs)
    update_start_end(start_end)
    for i in range(3):
        update_solution(i,[])
        update_dist(i,None)
    assert(len(locs) == y - 1)
    assert(start_end not in locs)

def choose_option():
    # use this for UI so user can choose algorithm
    prompt = "What would you like to do? \n \
    1: Run greedy \n \
    2: Run genetic \n \
    3: Run dynamic \n \
    4: View current path \n \
    5: Update number of cities \n \
    6: Update itinerary \n \
    0: Quit\n--> "
    x = int(raw_input(prompt))
    if x == 1:
        while get_cities() > 25:
            y = int(raw_input("Remember that the Greedy solution has a run time on the scale of O(n-1!), so please choose a smaller value for your cities! \n --> "))
            change_graph(y)
        t1 = time.time()
        greedy_result = greedy(get_graph())
        t2 = time.time()
        total_time = round(t2 - t1,3)

        greedy_sol = greedy_result[0]
        greedy_sol.remove(greedy_sol[0])
        greedy_sol = reorder_sol(0, greedy_result[0], get_start_end())
        update_solution(0, greedy_sol)
        update_dist(0, greedy_result[1])

        e_file.write("Greedy, time: "+str(total_time)+" for "+str(get_cities())+" cities \n")

        print "The minimum total distance is ", greedy_result[1]
        print "Greedy algorithm took "+ str(total_time)+" seconds."
    elif x == 2:
        global sols
        sols = []
        children = int(raw_input("How many rounds to run genetic? Please enter a number less than 2^25 to account for hardware limitations. \n --> "))
        print "Running... "

        t1 = time.time()
        gen_result = tsp_genetic(children, sols, get_graph(), get_start_end(), get_cities(), get_locs())
        t2 = time.time()
        total_time = round(t2 - t1,3)

        e_file.write("Genetic time: "+str(total_time)+" for "+str(get_cities())+" cities, "+str(children)+" crossovers \n")

        update_solution(1, gen_result[0])
        update_dist(1, gen_result[1])                        
        print "The best solution generated by the genetic algorithm has distance of",gen_result[1]
        print "Genetic algorithm took " + str(total_time) + " seconds."
    elif x == 3:
        while get_cities() > 25:
            y = int(raw_input("Remember that the Dynamic Programming solution takes space on the scale of O(n * 2^n) and run time on the scale of O(n^2 * 2^n), so please choose a smaller value! \n --> "))
            change_graph(y)
        t1 = time.time()
        dynamic_result = tsp_dynamic(get_graph())
        t2 = time.time()
        total_time = round(t2 - t1,3)

        e_file.write("Dynamic, time: "+str(total_time)+" for "+str(get_cities())+" cities \n")

        # standardize output so that solution does not include starting city
        dyn_sol = dynamic_result[0]
        dyn_sol.remove(dyn_sol[-1]) # since dynamic returns start, list of cities, start, we remove a duplicate start/end
        dyn_sol = reorder_sol(2, dyn_sol, get_start_end())
        update_solution(2, dyn_sol)
        update_dist(2, dynamic_result[1])

        print "The minimum total distance is ", dynamic_result[1]
        print "Dynamic algorithm took " + str(total_time) + " seconds."
    elif x == 4:
        y =int(raw_input("Which solution would you like to see? \n 1: greedy \n 2: genetic \n 3: dynamic \n --> "))
        if (y < 1 or y > 3):
            print "Sorry, this algorithm doesn't exist!"
            choose_option()
        else:
            if (get_dist(y-1)) == None:
                print "This algorithm has not yet been run on this set of cities yet!"
                choose_option()
            print_path(y-1)
    elif x == 5:
        y = int(raw_input("How many cities should be traveled to? This will randomize the cities again. \n--> "))
        change_graph(y)
    elif x == 6:
        y = int(raw_input(" 1: Load coordinates from cities.txt \n 2: Enter coordinates \n --> "))
        if y == 1:
            f = open('cities.txt','r')
            cities = f.read().splitlines()
            cities = filter(lambda x: x != "", cities)
            for i in range(len(cities)):
                cities[i] = ast.literal_eval(cities[i])
            update_cities(len(cities))
            update_start_end(cities[0])
            a = get_graph()
            a.update_points(cities)
            cities.remove(cities[0])
            update_locs(cities)
            clear_solution()
            f.close()
        elif y == 2:
            c = int(raw_input("How many cities will you travel to? This includes the initial city.\n--> "))
            while c < 2:
                c = int(raw_input("Please enter a number greater than 1! "))
            locations = []

            # get initial city
            x_init = int(raw_input("x-coordinate of initial city is: "))
            y_init = int(raw_input("y-coordinate of initial city is: "))
            city = (x_init,y_init)

            # get all the other cities
            for i in range(1,c):
                number = str(i + 1)
                x = int(raw_input("x-coordinate of city #"+number+" is: "))
                y = int(raw_input("y-coordinate of city #"+number+" is: "))
                locations.append((x,y))

            # update like everything (wipe solutions clean)
            assert (len(locations) == c-1)
            update_locs(locations)
            update_start_end(city)
            update_cities(c)
            clear_solution()
            a = get_graph()
            points = locations + [city]
            a.update_points(points)
        else:
            choose_option()
    elif x == 0:
        e_file.close()
        return

    choose_option()


def print_path(num):
    assert (num < 3 and num > -1)
    sol = get_solution(num)
    create_png(num)
    print "Current path for traveling between these",get_cities(),"cities is: "
    print " 1 ) ",get_start_end()
    for i in range(len(sol)):
        print "",i+2,") ",sol[i]
    print "",len(sol)+2,") ",get_start_end()
    print "Total distance traveled:",get_dist(num)
    return

def create_png(num):
    path = get_solution(num)
    city = get_start_end()
    path.append(city)
    size = (500,500)
    padding = (50,50)
    im = Image.new("RGB",size,(255,255,255))

    draw = ImageDraw.Draw(im)
    font = ImageFont.load_default()

    s = 4 #scale
    p = 50 #padding, shift map over to middle of image
    tp = 15 + p #shift over text padding a bit to account for vertices later        
    low_bound = 90
    color = (255 - low_bound) / (len(path) - 1) # use to change colors

    #draw edges
    for i in range(len(path) - 1):
        c1 = path[i]
        c2 = path[i+1]

        draw.line((s*c1[0]+p, s*c1[1]+p, s*c2[0]+p, s*c2[1]+p), fill = (0,0,0))
        #label each city with coordinates
        draw.text((s*c1[0]+tp, s*c1[1]+p), str(c1), font=font, fill = (0,0,i*color+low_bound))

    c1 = path[len(path)-1] #this is the starting city due to the way append works
    c2 = path[0]
    draw.line((s*c1[0]+p, s*c1[1]+p, s*c2[0]+p, s*c2[1]+p), fill = (0,0,0))
    draw.text((s*c1[0]+tp, s*c1[1]+p), str(c1), font=font, fill = (255,0,0))
    
    #draw vertices (that aren't the starting/ending)
    path.remove(city)
    for i in range(len(path)):
        pos = path[i]
        x = s*pos[0] + p
        y = s*pos[1] + p
        draw.ellipse((x-5, y-5, x+5, y+5), outline=(0,0,0), fill = ((0,0,(i*color+low_bound))))

    #draw starting/ending city with RED
    x = s*city[0] + p
    y = s*city[1] + p
    draw.ellipse((x-5, y-5, x+5, y+5), outline=(0,0,0), fill = (255,0,0))

    draw.text((10,10), "Distance: " + str(get_dist(num)), font=font, fill = (0,0,0))
    if num == 0:
        name = "greedy"
    elif num == 1:
        name = "genetic"
    else:
        name = "dynamic"
    filename = "tsp_"+name+".png"
    draw.text((10,20), "Algorithm used: " + name, font=font, fill = (0,0,0))

    del draw
    im.save(filename, "PNG")

    os.system(filename)
    
    print ".png drawn!"

# main body
def main():
    print("Initializing...")

    a, cities, locs, start_end, dist
    dist = [None, None, None]
    e_file = open('efficiency.txt','a')

    cities = int(raw_input("How many cities would you like to visit? Please only use integers. "))
    while (cities < 2):
        cities = int(raw_input("Please choose a number greater than 1! "))
        
    g = Graph(cities)
    locs = g.points
    start_end = locs.pop()
    assert(len(locs) == cities - 1)
    assert(start_end not in locs)

    choose_option()

if __name__ == "__main__":
    main()
