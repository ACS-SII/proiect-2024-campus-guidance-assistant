
from map import *
from utils import *
import os
import math
import copy

AVG_SPEED = 1.4 # meters per second

def expand(path, map):
    
    # Get the last station of the path
    lastStation = path.last
    
    # Create the list of paths that I will return at the end
    pathList = []
    
    # Get all the children of the last station in the given path from the map
    children = map.connections[lastStation].keys()

    for child in children:
        # Assuming time and distance are obtained from the map connections
        time = map.connections[lastStation][child]['time']
        distance = map.connections[lastStation][child]['distance']
        
        newPath = copy.deepcopy(path)
        newPath.add_route(child, time, distance)
        pathList.append(newPath)

    return pathList



def remove_cycles(path_list):

    # Creating a new list to store paths without cycles
    newList = []

    for path in path_list:
        
        # Checking if the last station in the path has been previously visited
        if path.last not in path.route[:-1]:
            newList.append(path)

    return newList



def calculate_cost(expand_paths, map):

    for path in expand_paths:
        penultStation = path.penultimate
        lastStation = path.last
        
        if penultStation is not None:
            # Directly use the cost from the map connections if penultStation is not None
            costs = map.connections[penultStation][lastStation]
            path.update_g_costs(costs)

    return expand_paths



def insert_cost(expand_paths, list_of_path):
    
    #Concatenate the two lists
    list_of_path = list_of_path + expand_paths
    
    #Sort the list ordered by the cummulative cost
    list_of_path.sort(key=lambda path: path.g_distance)
    
    return list_of_path
    


def uniform_cost_search(origin_id, destination_id, map):
    

    listOfPaths = [Path(origin_id)]
    
    while listOfPaths:
        c = listOfPaths[0]
        
        # Verifying if the path we are checking ends at destination
        # if yes, returning the path and exiting the loop
        if c.last == destination_id:
            break
        
        e = expand(c, map)
        r = remove_cycles(e)
        
        # if the path we are checking is not the goal, we remove it
        listOfPaths.remove(c)
        
        # computing the cumulative cost without type preference
        cost = calculate_cost(r, map)
        
        # inserting in list in cumulative cost order
        listOfPaths = insert_cost(cost, listOfPaths)
    
    if listOfPaths:
        return listOfPaths[0]
    else:
        return "No solution exists"

# NOT IMPLEMENTED ON OUR CASE, THIS IS JUST A TEMPLATE
# |
# |
# v 
def calculate_heuristics(expand_paths, map, destination_id, type_preference, weather, wind):    
    
    if type_preference == "distance" and weather == "sunny" and wind == 0:
        
        #Adjacency with no preferencies (classical ucs)
        for path in expand_paths:
            lastStation = path.last
            path.update_h(0)
                
    elif type_preference == 1:
        
        # The minimum Time will be computed using the euclidean distance and the maximum speed
        maxSpeed = 0
        for station_id, station in map.stations.items():
            if 'velocity' in station:
                maxSpeed = max(maxSpeed, station['velocity'])
                
                for path in expand_paths:
                    if path.last == destination_id:
                        path.update_h(0)
                    
                    else:
                        cur_station = map.stations[path.last]
                        dest_station = map.stations[destination_id]
                        distance = euclidean_dist([cur_station['x'], cur_station['y']], [dest_station['x'], dest_station['y']])
                        cost = distance / maxSpeed
                        path.update_h(cost)
                    
    elif type_preference == 2:
        
        # minimum Distance: euclidian distance
        for path in expand_paths:
            if path.last == destination_id:
                path.update_h(0)
                
            else:
                curStation = map.stations[path.last]
                destStation = map.stations[destination_id]
                cost = euclidean_dist([curStation['x'], curStation['y']], [destStation['x'], destStation['y']])
                path.update_h(cost)
            
                
                
    elif type_preference == 3:
        
        # minimum Transfers
            for path in expand_paths:
                lastStation = path.last
                if map.stations[lastStation]['line'] != map.stations[destination_id]['line']:
                    path.update_h(1)
                else:
                    path.update_h(0)
    # Return the updated list of paths.
    return expand_paths

def update_f(expand_paths): 
    
    for path in expand_paths:
        path.update_f()
        
    return expand_paths

def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost): 
      
    for path in expand_paths:
        lastStation=path.last
        
        if lastStation in visited_stations_cost and path.g >= visited_stations_cost[lastStation]:
            # if is a redundant path if the cost of the path we are at is bigger than the cost of
            # the last station wewe were at

            expand_paths.remove(path)
            
        else:
            #if the cost is smaller, we change the cost of the last station visited
            
            visited_stations_cost[lastStation] = path.g
            
            
            for elem in list_of_path:
                if lastStation in elem.route:
                    # if the lastStation is already in the route/visited, we don't count
                    # it again --> we remove it from the list

                    list_of_path.remove(elem)

    return expand_paths, list_of_path, visited_stations_cost

def insert_cost_f(expand_paths, list_of_path): 
    
    #Concatenate the two lists
    list_of_path = list_of_path + expand_paths
    
    #Sort the list ordered by the total cost
    list_of_path.sort(key=lambda path: path.f)
    
    return list_of_path

def coord2station(coord, map):
    
    # The list of IDs
    listOfClosestStation = []
    
    minimumDistance = float('inf')
    
    for id, station in map.stations.items():
        
        # Computing the distance
        stationCoord = [station['x'],station['y']]
        distance = euclidean_dist(stationCoord, coord)
        
        # If there is a new minimum, we rewrite the list from scratch 
        if distance < minimumDistance:
            listOfClosestStation = [id]
            minimumDistance = distance
        
        # If there is a station with the same distance, we add it to the list
        elif distance == minimumDistance:
            listOfClosestStation.append(id)
    
    return listOfClosestStation
    
    pass


def Astar(origin_id, destination_id, map, type_preference=0):
    
    origin = map.stations[origin_id]
    destination = map.stations[destination_id]
    
    originCoord = (origin['x'],origin['y'])
    listOfPaths = [Path((coord2station(originCoord,map))[0])]
    
    destCoord = (destination['x'],destination['y'])
    destination = coord2station(destCoord, map)[0]
    costs = {}
    
    while listOfPaths:
        c = listOfPaths[0]
        
        #Verifying if the path we are checking ends at destination
        #if yes, returning the path and exiting the loop
        if c.last == destination_id:
            break
        
        e = expand(c, map)
        r = remove_cycles(e)
        
        # if the path we are checking is not the goal, we remove it
        listOfPaths.remove(c)
        print(listOfPaths)
        
        # computing the total cost step by step
        cumulativeCost = calculate_cost(r, map,type_preference)
        print("cumulTIVE:",cumulativeCost)
        heuristicCost = calculate_heuristics(cumulativeCost, map, destination, type_preference)
        print("h:",heuristicCost)
        totalCost = update_f(heuristicCost)
        
        # removing the redundancy and insterting using total cost order
        noRedundacy, listOfPaths, costs = remove_redundant_paths(totalCost, listOfPaths, costs)
        listOfPaths = insert_cost_f(noRedundacy, listOfPaths)
        
    if listOfPaths:
        return listOfPaths[0]
    else:
        return "No solution exists"

# city_map = Map()
# city_map.load_from_json(r"jsonFiles\stations.json")
# print(city_map.stations[19]["z"])