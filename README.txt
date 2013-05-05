README

- This project is implemented in Python 2.7.x, and requires that the Python Imaging Library is installed.
- To run the project, simply run Projects.py. We ask that ALL input be in integer form, ex. "five" is not acceptable input, but 5 is.
- The program will, when run, initialize and ask the user for an initial value for the number, n, of cities that will be solved on. This will generate n random cities whose coordinates are within (0,0) and (100,100). This data set can be changed at any time.
- The user then has six options to choose from. The user can run one of three algorithms on the randomly generated data set, print the solution stored by the latest iteration of any of the three algorithms (if one has been run on the current data set), generate a new set of n random cities (where n is determiend by the user), or give the program a a set of cities either by reading locations stored in cities.txt or manually entering coordinates into the command line. The user can also choose to terminate the program.

Overall notices:
- The only inputs accepted by our program are INTEGERS. Please do not enter floats, strings, etc of any kind!
- We ask that the user run our program on a data set of 2-25 cities, due to hardware limitations (ex. the dynamic programming algorithm handles integers of 2^n, where n is the number of cities, and as Python is 32-bit, it will promptly crash if it tries to operate on more than 32 cities, so we've chosen to limit the number of cities to 25. While genetic can run on larger sets, the visualization of percent error will not be accurate.

Specific directions by option:

1. Greedy
- The greedy algorithm should run without additional user input, unless the number of cities in the data set is greater than 25, at which point it will prompt the user to give it a smaller (randomly generated) data set.

2. Genetic
- The genetic algorithm will ask the user how many "rounds" to run genetic. Each round represents one call to a crossover function and a certain percent chance (currently 10%) of one call to a mutation function. These are not determined by the user, but are adjusted in the code for tsp_genetic. The genetic algorithm will start to require more time around 500 or 1000 rounds.

3. Dynamic
- The dynamic algorithm should run without additional user input, unless the number of cities in the data set is greater than 25, at which point it will prompt the user to give it a smaller (randomly generated) data set.

4. Printing the path
- On choosing option 4, the user will be asked which algorithm's solution to print. If the algorithm the user chooses has not been run on the current data set, nothing will be printed. If there is an existing solution for that algorithm and data set, the program will then create a .png file displaying a map of the cities with the solution path drawn between them and the initial city drawn in red. The program will also print the coordinates of the path in the command line and label each coordinate pair with what order they are visited, as well as the total distance traveled, as well as the length of the path in red compared to the baseline path in blue, where we use the result from the dynamic programming algorithm as the baseline.

5. Update number of cities
- This option prompts the user for a number n. It then generates a new graph with n random cities. There is no upper limit on n because the algorithms will check the number of cities in their own options, allowing genetic to run on larger sets but greedy and dynamic will not.

6. Update itinerary
- The user is asked if they would like to load coordinates in cities.txt or manually enter in coordinates. If they choose to manually enter coordinates, the user is then asked how many cities they would like to visit before entering in the x and y coordinates for each city. Because this is time-consuming for larger graphs, the user also has the option of using coordinates stored in cities.txt, which must be in the format (x,y) with one coordinate pair per line. 
