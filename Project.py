from tsp_genetic_Alex import *
from tsp_dynamic import *
from greedy import *
from PIL import Image, ImageDraw, ImageFont
import time, os

solution = ([],[],[])
#solution[0] = greedy, solution[1] = genetic, solution[2] = dynamic

def update_solution(num, newsol):
    global solution
    if num == 0:
        solution = (newsol,) + solution[1:3]
    elif num == 1:
        solution = solution[0:1] + (newsol,) + solution[2:3]
    elif num == 2:
        solution = solution[0:2] + (newsol,)
    else:
        print "Error: num is not in range!"
    return

def update_cities(n):
    global cities
    while n < 2:
        n = int(raw_input("Please enter a number greater than 1! "))
    cities = n
    return

def update_graph(n):
    global a
    a = Graph(n)
    return

def update_locs(lst):
    global locs
    locs = lst
    return

def update_start_end(city):
    global start_end
    start_end = city
    return

def update_dist(num, n):
    global dist
    if num == 0:
        dist = (n,) + dist[1:3]
    elif num == 1:
        dist = dist[0:1] + (n,) + dist[2:3]
    elif num == 2:
        dist = dist[0:2] + (n,)
    else:
        print "Error: num is not in range!"
    return

def get_solution(num):
    global solution
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
    # given a solution and an initial city, reorders list so that
    # initial city is at the front but otherwise unchanged
    # except it returns all the cities *after* initial
    assert initial in sol
    x = sol.index(initial)
    newsol = sol[x+1:] + sol[:x]
    return newsol

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
        if x > 25:
            y = int(raw_input("Remember that the Greedy solution has a \n \
            run time on the scale of O(n-1!), so please choose a smaller value!"))
            update_cities(y)
            update_graph(y)
        t1 = time.time()
        greedy_result = greedy(get_graph())
        t2 = time.time()
        total_time = round(t2 - t1,3)

        greedy_sol = greedy_result[0]
        greedy_sol.remove(greedy_sol[0])
        greedy_sol = reorder_sol(0, greedy_result[0], get_start_end())
        update_solution(0, greedy_sol)
        update_dist(0, greedy_result[1])

        print "The minimum total distance is ", greedy_result[1]
        print "Greedy algorithm took "+ str(total_time)+" seconds."
    elif x == 2:
        global sols
        sols = []
        children = int(raw_input("How many rounds to run genetic? Please enter a number less than 2^25 to account for hardware limitations. ",))
        print "Running... "

        t1 = time.time()
        gen_result = tsp_genetic(children, sols, get_graph(), get_start_end(), get_cities(), get_locs())
        t2 = time.time()
        total_time = round(t2 - t1,3)

        update_solution(1, gen_result[0])
        update_dist(1, gen_result[1])                        
        print "The best solution generated by the genetic algorithm has distance of",gen_result[1]
        print "Genetic algorithm took " + str(total_time) + " seconds."
    elif x == 3:
        if x > 25:
            y = int(raw_input("Remember that the Dynamic Programming solution takes space on the scale of O(n * 2^n) and \
                 run time on the scale of O(n^2 * 2^n), so please choose a smaller value!"))
            update_cities(y)
            update_graph(y)
        t1 = time.time()
        dynamic_result = tsp_dynamic(get_graph())
        t2 = time.time()
        total_time = round(t2 - t1,3)

        # standardize output so that solution does not include starting city
        dyn_sol = dynamic_result[0]
        dyn_sol.remove(dyn_sol[-1]) # since dynamic returns start, list of cities, start, we remove a duplicate start/end
        dyn_sol = reorder_sol(2, dyn_sol, get_start_end())
        update_solution(2, dyn_sol)
        update_dist(2, dynamic_result[1])

        print "The minimum total distance is ", dynamic_result[1]
        print "Dynamic algorithm took " + str(total_time) + " seconds."
    elif x == 4:
        y =int(raw_input("Which solution would you like to see? \n \
        1: greedy \n \
        2: genetic \n \
        3: dynamic \n \
        --> "))
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
    elif x == 6:
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
        for i in range(r):
            update_solution(i, [])
            update_dist(i, None)
        # need to update the graph somehow or change how dynamic and greedy take inputs
        a = get_graph()
        points = locations + [city]
        a.update_points(points)
    elif x == 0:
        return

    choose_option()


def print_path(num):
    assert (num < 3 and num > -1)
    sol = get_solution(num)
    sol = sol[num]
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

    global a, cities, locs, start_end, dist
    dist = (None, None, None)

    prompt1 = "How many cities would you like to visit? "
    cities = int(raw_input(prompt1))
    while (cities < 2):
        cities = int(raw_input("Please choose a number greater than 1! "))
    a = Graph(cities)
    locs = a.points
    start_end = locs[0]
    locs.remove(start_end)
    assert(len(locs) == cities - 1)
    assert(start_end not in locs)

    choose_option()

if __name__ == "__main__":
    main()
