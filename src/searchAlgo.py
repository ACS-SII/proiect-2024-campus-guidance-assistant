
from mapa import *
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
def calculate_heuristics(expand_paths, map, destination_id, type_preference = "distance", weather = "sunny"):    
    
    if weather == "sunny":

        h_costs = {}

        if 'time' not in h_costs:
            h_costs['time'] = 0
        if 'distance' not in h_costs:
            h_costs['distance'] = 0
        
        for path in expand_paths:
            
            if type_preference == "distance":
            #Adjacency with no preferencies (heurisitics without any penalties)
                cur_station = map.stations[path.last]
                dest_station = map.stations[destination_id]
                distance = euclidean_dist(
                    [cur_station['x'],dest_station['x']],
                    [cur_station['y'],dest_station['y']],
                    [cur_station['z'],dest_station['z']])

                h_costs['distance'] = distance
        
            elif type_preference == "time":
                cur_station = map.stations[path.last]
                dest_station = map.stations[destination_id]
                distance = euclidean_dist(
                    [cur_station['x'],dest_station['x']],
                    [cur_station['y'],dest_station['y']],
                    [cur_station['z'],dest_station['z']])
                
                time = distance/AVG_SPEED
                h_costs['time'] = time
        
            path.update_h_costs(h_costs)

    if weather == "rainy":

        h_costs = {}

        if 'time' not in h_costs:
            h_costs['time'] = 0
        if 'distance' not in h_costs:
            h_costs['distance'] = 0
        
        for path in expand_paths:
            
            if type_preference == "distance":
            #Adjacency with no preferencies (heurisitics without any penalties)
                cur_station = map.stations[path.last]
                dest_station = map.stations[destination_id]
                distance = euclidean_dist(
                    [cur_station['x'],dest_station['x']],
                    [cur_station['y'],dest_station['y']],
                    [cur_station['z'],dest_station['z']])
                
                rain_penalty = 0.5
                distance += rain_penalty

                h_costs['distance'] = distance
        
            elif type_preference == "time":
                cur_station = map.stations[path.last]
                dest_station = map.stations[destination_id]
                distance = euclidean_dist(
                    [cur_station['x'],dest_station['x']],
                    [cur_station['y'],dest_station['y']],
                    [cur_station['z'],dest_station['z']])
                
                rain_penalty = 0.5
                distance += rain_penalty

                time = distance/AVG_SPEED
                h_costs['time'] = time
        
            path.update_h_costs(h_costs)
    
    if weather == "snowy":

        h_costs = {}

        if 'time' not in h_costs:
            h_costs['time'] = 0
        if 'distance' not in h_costs:
            h_costs['distance'] = 0
        
        for path in expand_paths:
            
            if type_preference == "distance":
            #Adjacency with no preferencies (heurisitics without any penalties)
                cur_station = map.stations[path.last]
                dest_station = map.stations[destination_id]
                distance = euclidean_dist(
                    [cur_station['x'],dest_station['x']],
                    [cur_station['y'],dest_station['y']],
                    [cur_station['z'],dest_station['z']])
                
                snow_penalty = 1.5
                distance += snow_penalty

                h_costs['distance'] = distance
        
            elif type_preference == "time":
                cur_station = map.stations[path.last]
                dest_station = map.stations[destination_id]
                distance = euclidean_dist(
                    [cur_station['x'],dest_station['x']],
                    [cur_station['y'],dest_station['y']],
                    [cur_station['z'],dest_station['z']])
                
                snow_penalty = 1.5
                distance += snow_penalty
                
                time = distance/AVG_SPEED
                h_costs['time'] = time
        
            path.update_h_costs(h_costs)

    return expand_paths

def update_f(expand_paths): 
    
    for path in expand_paths:
        path.update_f_costs()
        
    return expand_paths

def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost,type_preference = "distance"): 
      
    for path in expand_paths:
        lastStation=path.last
        if type_preference == "distance":
            if lastStation in visited_stations_cost and path.g_distance >= visited_stations_cost[lastStation]:
            # if is a redundant path if the cost of the path we are at is bigger than the cost of
            # the last station wewe were at

                expand_paths.remove(path)
            
            else:
            #if the cost is smaller, we change the cost of the last station visited
                visited_stations_cost[lastStation] = path.g_distance
            
            for elem in list_of_path:
                if lastStation in elem.route:
                    # if the lastStation is already in the route/visited, we don't count
                    # it again --> we remove it from the list

                    list_of_path.remove(elem)

        if type_preference == "time":
            if lastStation in visited_stations_cost and path.g_time >= visited_stations_cost[lastStation]:
            # if is a redundant path if the cost of the path we are at is bigger than the cost of
            # the last station wewe were at

                expand_paths.remove(path)
            
            else:
            #if the cost is smaller, we change the cost of the last station visited
                visited_stations_cost[lastStation] = path.g_time
            
            for elem in list_of_path:
                if lastStation in elem.route:
                    # if the lastStation is already in the route/visited, we don't count
                    # it again --> we remove it from the list

                    list_of_path.remove(elem)
    return expand_paths, list_of_path, visited_stations_cost

def insert_cost_f(expand_paths, list_of_path, type_preference = "distance"): 
    
    #Concatenate the two lists
    list_of_path = list_of_path + expand_paths
    
    if type_preference == "distance":
        #Sort the list ordered by the total cost
        list_of_path.sort(key=lambda path: path.f_distance)
    
    if type_preference == "time":
        list_of_path.sort(key=lambda path: path.f_time)
    
    return list_of_path

def coord2station(coord, map):
    
    # The list of IDs
    listOfClosestStation = []
    
    minimumDistance = float('inf')
    
    for id, station in map.stations.items():
        
        # Computing the distance
        stationCoord = [station['x'],station['y'],station['z']]
        distance = euclidean_dist([stationCoord[0],coord[0]],[stationCoord[1],coord[1]],[stationCoord[2],coord[2]])
        
        # If there is a new minimum, we rewrite the list from scratch 
        if distance < minimumDistance:
            listOfClosestStation = [id]
            minimumDistance = distance
        
        # If there is a station with the same distance, we add it to the list
        elif distance == minimumDistance:
            listOfClosestStation.append(id)
    
    return listOfClosestStation

def Astar(origin_id, destination_id, map, type_preference = "distance", weather = "sunny"):
    
    origin = map.stations[origin_id]
    destination = map.stations[destination_id]
    
    originCoord = (origin["x"],origin["y"], origin["z"])
    listOfPaths = [Path((coord2station(originCoord,map))[0])]
    
    destCoord = (destination['x'],destination['y'],destination['z'])
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
        cumulativeCost = calculate_cost(r, map)
        print("cumulTIVE:",cumulativeCost)
        heuristicCost = calculate_heuristics(cumulativeCost, map, destination, type_preference,weather)
        print("h:",heuristicCost)
        totalCost = update_f(heuristicCost)
        
        # removing the redundancy and insterting using total cost order
        noRedundacy, listOfPaths, costs = remove_redundant_paths(totalCost, listOfPaths, costs,type_preference)
        listOfPaths = insert_cost_f(noRedundacy, listOfPaths, type_preference)
        
    if listOfPaths:
        return listOfPaths[0]
    else:
        return "No solution exists"

# city_map = Map()
# city_map.load_from_json(r"jsonFiles\stations.json")
# my_path = Astar(1,6,city_map,"distance")
# #my_path = uniform_cost_search(1,6,city_map)
# print("LISTA DE STATII:\n")
# #print(my_path)
# print(f"the x of the id=1 is: {city_map.stations[1]['x']}")
# current_path =[]
# for station_id in my_path.route:
#         current_path.append(city_map.stations[station_id]['name'])
# #print(current_path)