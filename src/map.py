import json

class Map:
    def __init__(self):
        self.stations = {}  # Holds info about locations: {id: {"name": name, "type": type_of_location}}
        self.connections = {}  # Holds cost information between locations
        self.directions = {} # Holds the direction information for every checkpoint and its connection
    def load_from_json(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
            for station in data["stations"]:
                self.add_station(station["id"], station["name"], station["type"], station["x"], station["y"], station["z"])
            
            for connection in data["connections"]:
                self.add_connection(connection["station1_id"], connection["station2_id"], connection["cost"])
            
            for direction in data["directions"]:
                self.add_direction(direction["from"], direction["to"],direction["direction"])
    def add_station(self, id, name, type_of_location, x, y, z):
        self.stations[id] = {'name': name, 'type': type_of_location, 'x':x, 'y':y, 'z':z}

    def add_connection(self, station1_id, station2_id, cost):
        if station1_id not in self.connections:
            self.connections[station1_id] = {}
        if station2_id not in self.connections:
            self.connections[station2_id] = {}
    
        # Assuming bidirectional connection with the same cost
        self.connections[station1_id][station2_id] = cost
        self.connections[station2_id][station1_id] = cost

    def add_direction(self, station1_name, station2_name, direction):
        name = station1_name + "-" + station2_name
        if name not in self.directions:
            self.directions[name] = []
        self.directions[name]=direction
        
class Path:
    def __init__(self, route):
        if isinstance(route, list):
            self.route = route
        else:
            self.route = [route]

        self.head = self.route[0]
        self.last = self.route[-1]
        self.penultimate = self.route[-2] if len(self.route) >= 2 else None
        self.g_time = 0  # Real time
        self.g_distance = 0  # Real distance
        self.h_time = 0 # Heuristic cost in time
        self.h_distance = 0 # Heuristic cost in distance
        self.f_time = 0 # Sum of g_time and h_time
        self.f_distance = 0 # Sum of g_distance and h_distance

    def add_route(self, next_station, time, distance):
        # Adding a new station to the route list and updating costs
        self.route.append(next_station)
        self.last = next_station
        self.g_time += time
        self.g_distance += distance

    def update_g_costs(self, g_costs):
        # Method to manually update costs if needed
        self.g_time += g_costs["time"]
        self.g_distance += g_costs["distance"]
    
    def updatee_h_costs(self, h_costs):
        self.h_time = h_costs["time"]
        self.h_distance = h_costs["distance"]

    def update_f_costs(self):
        self.f_time = self.g_time + self.h_time
        self.f_distance = self.g_distance + self.h_distance 
