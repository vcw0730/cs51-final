from tsp_genetic import *
from tsp_dynamic import *
from greedy import *
from PIL import Image, ImageDraw
import time

solution = []

def update_solution(newsol):
    global solution
    solution = newsol
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

def update_dist(n):
    global dist
    dist = n
    return

def get_solution():
    global solution
    return solution

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

def get_dist():
    global dist
    return dist

def reorder_sol(sol,initial):
    # given a solution and an initial city, reorders list so that
    # initial city is at the front but otherwise unchanged
    # except it returns all the cities *after* initial
    assert initial in sol
    x = sol.index(initial)
    newsol = sol[x+1:] + sol[:x]
    update_solution(newsol)
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
    7: Change initial city \n \
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

        # probably needs to be changed depending on how greedy is implemented
        greedy_sol = reorder_sol(greedy_result[0],get_start_end())
        greedy_sol.remove(greedy_sol[0])
        update_solution(greedy_sol)
        update_dist(greedy_result[1])

        print "The minimum total distance is ", greedy_result[1]
        print "Greedy algorithm took "+ str(total_time)+" seconds."
    elif x == 2:
        global sols
        sols = []
        t1 = time.time()
        run_genetic()
        t2 = time.time()
        total_time = round(t2 - t1,3)

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
        dyn_sol = reorder_sol(dyn_sol,get_start_end())
        update_solution(dyn_sol)
        update_dist(dynamic_result[1])

        print "The minimum total distance is ", dynamic_result[1]
        print "Dynamic algorithm took " + str(total_time) + " seconds."
    elif x == 4:
        if get_dist() == None:
            print "No algorithm has been run on this set of cities yet!"
            choose_option()
        print_path()
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
        update_solution([])
        update_dist(None)
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
        update_solution([])
        update_dist(None)
        # need to update the graph somehow or change how dynamic and greedy take inputs
    elif x == 7:
        if get_dist() == None:
            print "No algorithm has been run on this set of cities yet!"
            choose_option()

        sol = get_solution()
        y = int(input("Which city out of the current solutions do you want to make the initial city? Enter its position in the current path.\n--> "))
        while (y < 1 or y > len(sol) + 2):
            y = int(raw_input("Try again! "))
        if y == 1 or y == len(sol) + 2:
            choose_option()
        sol_ind = y-2
        city = sol[sol_ind]
        sol.append(get_start_end())
        newsol = reorder_sol(sol,city)

        update_solution(newsol)
        update_start_end(city)
    elif x == 0:
        return

    choose_option()

def run_genetic():    
    gen_population(get_cities(), get_locs(), sols)
    children = int(raw_input("How many rounds to run genetic? "))
    print "Running... "
    run_gen(children,sols,get_graph(),get_start_end(),get_cities(),get_locs())
    x = best_sol(sols,get_graph(),get_start_end())
    solution = sols[x]
    update_solution(solution)
    dist = solution_len(solution,get_graph(),get_start_end())
    update_dist(dist)                        
    print "The best solution generated by the genetic algorithm is number",x,"with distance of",dist
    return

def print_path():
    sol = get_solution()
    create_png()
    print "Current path for traveling between these",get_cities(),"cities is: "
    print " 1 ) ",get_start_end()
    for i in range(len(sol)):
        print "",i+2,") ",sol[i]
    print "",len(sol)+2,") ",get_start_end()
    print "Total distance traveled:",get_dist()
    return

def create_png():
    path = get_solution()
    path.append(get_start_end())
    size = (500,500)
    padding = (50,50)
    im = Image.new("RGB",size,(255,255,255))

    draw = ImageDraw.Draw(im)

    s = 4 #scale
    p = 50 #padding, shift map over to middle of image

    #draw edges
    for i in range(len(path) - 1):
        c1 = path[i]
        c2 = path[i+1]
        draw.line((s*c1[0]+p,s*c1[1]+p,s*c2[0]+p,s*c2[1]+p), fill = (0,0,0))
    c1 = path[0]
    c2 = path[len(path)-1]
    draw.line((s*c1[0]+p,s*c1[1]+p,s*c2[0]+p,s*c2[1]+p), fill = (0,0,0))
    
    #draw vertices
    for i in path:
        x = s*i[0] + p
        y = s*i[1] + p
        draw.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill = (255,255,255))

    del draw
    im.save("tsp_map.png", "PNG")
    path.remove(get_start_end())
    print ".png drawn!"

# main body
def main():
    print("Initializing...")

    global a, cities, locs, start_end, dist
    dist = None

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
