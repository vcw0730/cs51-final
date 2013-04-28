from tsp_genetic import *
from shortest_path_withlog import *

solution = []

# genetic values
sols = []
cities = 5
a = Graph(5)
locs = a.points
start_end = locs[0]
locs.remove(locs[0])

def update_solution(newsol):
    global solution
    solution = newsol
    return

def update_cities(n):
    global cities
    while n < 2:
        n = int(input("Please enter a number greater than 1! "))
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

def choose_option():
    # use this for UI so user can choose algorithm
    prompt = """What would you like to do?
    1: Run genetic
    2: Run dynamic
    3: View current path
    4: Update number of cities
    5: Update itinerary
    6: Change initial city
    0: Quit\n--> """
    x = int(input(prompt))
    if x == 0:
        return
    if x == 1:
        global sols
        sols = []
        run_genetic()
    # if x == 2: clear solutions, run dynamic
    if x == 3:
        print_path()
    if x == 4:
        y = int(input("How many cities should be traveled to? This will randomize the cities again. \n--> "))
        update_cities(y)
        update_graph(y)
        locs = a.points
        start_end = locs[0]
        locs.remove(start_end)
        update_locs(locs)
        update_start_end(start_end)
        assert(len(locs) == y - 1)
        assert(start_end not in locs)
    if x == 5:
        cities = int(input("How many cities will you travel to? This does not include the initial city.\n --> "))
        locations = []
        for i in range(1,cities+1):
            number = str(i)
            x = int(input("X-coordinate of city "+number+" is: "))
            y = int(input("Y-coordinate of city "+number+" is: "))
            locations.append((x,y))
        assert (len(locations) == cities)
        update_locs(locations)
        update_cities(cities+1)
    if x == 6:
        y = int(input("Which city out of the current solutions do you want to make the intial city? Enter its position in the current path.\n --> "))
        while (y < 1 or y > len(solution) + 2):
            y = int(input("Try again! "))
        if y == 1 or y == len(solution) + 2:
            choose_option()
        city = solution[y-2]
        temp = get_start_end()
        solution[y-2] = temp
        locs = get_locs()
        locs[locs.index(city)] = temp
        update_start_end(city)
        update_locs(locs)

    choose_option()

def run_genetic():    
    gen_population(get_cities(), get_locs(), sols)
    children = int(input("How many rounds to run genetic? "))
    print ("Running... ")
    run_gen(children,sols,get_graph(),get_start_end(),get_cities(),get_locs())
    x = best_sol(sols,get_graph(),get_start_end())
    solution = sols[x]
    update_solution(solution)
    print ("The best solution generated by the genetic algorithm is number", x,
       "with distance of", solution_len(solution,a,get_start_end()))
    return

def print_path():
    global solution
    print ("Current path for traveling between these",get_cities(),"cities is: ")
    print (" 1 )",get_start_end())
    for i in range(len(solution)):
        print ("",i+2,")",solution[i])
    print ("",len(solution)+2,")",get_start_end())
    distance = solution_len(solution,get_graph(),get_start_end())
    print ("Total distance traveled:",distance)
    return


# main body
print("Initializing...")

prompt1 = "How many cities would you like to visit? "
cities = int(input(prompt1))
while (cities < 2):
    cities = int(input("Please choose a number greater than 1! "))
a = Graph(cities)
locs = a.points
start_end = locs[0]
locs.remove(start_end)

choose_option()

