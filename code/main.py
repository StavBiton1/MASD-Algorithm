import datetime
import random
from create_packages import create_packages
from storage_places import storage_location
from create_graph import graph
import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import pairwise
import csv
from visualise import Map, Agent, Animation
import pygame
import pandas as pd
from itertools import zip_longest
import time 

s_time = time.time()

packages= 25 #number of packages
shelves=3 #number of shelves
shelvesRow=3 #number of rows of shelves
TodayDate = datetime.date.today() # the date of today
numberOfagent=4 #The total number of agents (who reach only the low shelves and who reach both of the heights of the shelves)
liftupagent=2 #Agents that can reach the low and high shelves

# function to create agent. arguments - total number of agents, number of agents that can reach high shelves
def create_agents(num_agents, num_level2):
    agents = []
    for i in range(num_agents):
        lift_up = False
        if i < num_level2:
            lift_up = True
        serial_number = i + 1
        path = []
        allocate = False
        now = datetime.datetime.now()
        des_location = {"location": (-1,i), "time": now.replace(hour=0, minute=0, second=0, microsecond=0)}
        agent = {
            "serial_number": serial_number,
            "lift_up": lift_up,
            "path": path,
            "allocate": allocate,
            "des_location": des_location,
        }
        agents.append(agent)
    return agents

# function for update the date in packages list. after allocate old packages update tha data in the general package list
def update_package_data(old_packages, my_packages):
    for old_package in old_packages:
        for package in my_packages:
            if package['storage_id'] == old_package['storage_id']:
                # Update the storage_id and state data
                package["storage_id"] = old_package["storage_id"]
                package["state"] = old_package["state"]
                break  # Exit the inner loop once the package has been updated

# function for return storage location from allocation to free list 
def Free_storage_location(package, A_list, B_list, C_list, allocate_list):
    if package["storage_id"][0] == "A":
        A_list.append(package["storage_id"])
        allocate_list.remove(package["storage_id"])
    elif package["storage_id"][0]=="B":
        B_list.append(package["storage_id"])
        allocate_list.remove(package["storage_id"])
    else:
        C_list.append(package["storage_id"])
        allocate_list.remove(package["storage_id"]) 

agents=create_agents(4, 2) # create agents
for agent in agents:
    agent["path"].append(agent["des_location"]["location"])
    agent["path"].append(0)

start_of_day = datetime.datetime.combine(TodayDate, datetime.time.min )

# create graph frm csv
csv_file = "../code/small_map.csv"
new_csv="../code/map.csv"
G, names, pos = graph.create_graph_from_csv(new_csv)

#create packages 
my_packages = create_packages.split_packages(packages)

#create lists of the storage location
A_list,B_list,C_list = storage_location.storage_spaces(shelves,shelvesRow)

allocate_list=[]

# Create list of packages that are in the warehouse allready. 
old_packages = [
    package for package in my_packages
    if package["income_time"].date() < TodayDate
    and package["outcome_time"].date() >= TodayDate
]

# Update the location of old packages in the wharehose in the total package list
old_packages, A_list, B_list, C_list, allocate_list = storage_location.AllocateOldPackages(old_packages, A_list, B_list, C_list, allocate_list)
update_package_data(old_packages,my_packages)

# list of all the packages that come in/out today
today_packages = [
    package for package in my_packages
    if package["income_time"].date() == TodayDate
    or package["outcome_time"].date() == TodayDate
]

# Sort the filtered packages by time of today
sorted_packages = sorted(today_packages, key=lambda package: package["income_time"].time() if package["income_time"].date() == TodayDate else package["outcome_time"].time())

# Define the time intervals for processing packages
interval_start = start_of_day
interval_end = start_of_day + datetime.timedelta(minutes=30)

# Process packages for each 5-minute interval of the day
while interval_start < start_of_day + datetime.timedelta(days=1):
    packages_in_interval = [
        package for package in sorted_packages
        if interval_start.time() <= (package["income_time"].time() if package["income_time"].date() == TodayDate else package["outcome_time"].time()) < interval_end.time()
    ]
    entry_points = [(0, 6), (0, 7)] # point of the entry points in the graph
    num_entry_points = len(entry_points)
    current_entry_point_index = 0
    current_entry_point=(6,0)


    for package in packages_in_interval:
        # path planing for packages that income to the warhouse
        if package["income_time"].date() == TodayDate:
            current_entry_point = entry_points[current_entry_point_index]
            distances = []
            for agent in agents:
                if agent["des_location"]["time"] <= package["income_time"]:
                    distance = graph.manhattan_distance(current_entry_point, agent["des_location"]["location"])
                    distances.append(distance)
                else:
                    distance = 10000000000000
                    distances.append(distance)
            min_index = distances.index(min(distances))
            AgentForTask=agents[min_index]
            print(min_index , AgentForTask["des_location"]["location"],current_entry_point )
            AgentForTask = graph.find_path(G, names, pos,agents, AgentForTask, AgentForTask["des_location"]["location"], current_entry_point, package["income_time"])

            # Update the current entry point index for the next package
            current_entry_point_index = (current_entry_point_index + 1) % num_entry_points

            package, A_list, B_list, C_list, allocate_list = storage_location.AllocateNewPackages(package, A_list, B_list, C_list, allocate_list, AgentForTask)
            if package["storage_id"].endswith("1"):
                goal = package["storage_id"][:-1] + "0"
            else:
                goal = package["storage_id"]
            goal= graph.get_key_from_value(names, goal)
            print( AgentForTask["des_location"]["location"],goal, "storage_id", package["storage_id"])
            AgentForTask = graph.find_path(G, names, pos,agents, AgentForTask, AgentForTask["des_location"]["location"], goal, AgentForTask["des_location"]["time"])    
            #return to his first place
            AgentForTask = graph.find_path(G, names, pos, agents, AgentForTask, goal, (-1,AgentForTask["serial_number"]-1), AgentForTask["des_location"]["time"])    

            print("Processing")
        # path planing for packages that outcome from the warehouse
        else:
            distances = []
            if package["storage_id"].endswith("1"):
                start = package["storage_id"][:-1] + "0"
            else:
                start = package["storage_id"]
            start= graph.get_key_from_value(names, start)
            print("storage_id", package["storage_id"] , start)
            for agent in agents:
                if agent["des_location"]["time"] <= package["outcome_time"]:
                    distance = graph.manhattan_distance(start, agent["des_location"]["location"])
                    distances.append(distance)
                else:
                    distance = 100000000
                    distances.append(distance)
            min_index = distances.index(min(distances))
            AgentForTask=agents[min_index]
           
            print(min_index , AgentForTask["des_location"]["location"],start, "storage_id", package["storage_id"] )
            AgentForTask = graph.find_path(G, names, pos,agents, AgentForTask, AgentForTask["des_location"]["location"], start, package["outcome_time"])
            Free_storage_location(package, A_list, B_list, C_list, allocate_list)

            #package, A_list, B_list, C_list, allocate_list = storage_location.AllocateNewPackages(package, A_list, B_list, C_list, allocate_list, AgentForTask)
            print( AgentForTask["des_location"]["location"],(0,8))
            AgentForTask = graph.find_path(G, names, pos, agents, AgentForTask, AgentForTask["des_location"]["location"], (0,8), AgentForTask["des_location"]["time"])    
            
            #return to his first place
            AgentForTask = graph.find_path(G, names, pos, agents, AgentForTask, (0,8), (-1,AgentForTask["serial_number"]-1), AgentForTask["des_location"]["time"])    


   # if len(packages_in_interval)==1:

   #     print("Processing")
  #  else:
 #       print("Processing")

    for package in packages_in_interval:
        print(package)
    interval_start = interval_end
    interval_end += datetime.timedelta(minutes=30)

    print(agents[1]["path"])



# function that convert the path for the networkx grid to pygame grid format
def convert_path(path):
    converted_path = []
    for i in range(0, len(path)):
        if isinstance(path[i], tuple):
            x = path[i][0]
            y = 10 - path[i][1]
            converted_path.append((x, y))
        else:
            converted_path.append(path[i])
    return converted_path

def format_agent_data(all_agent_data_str):
    formatted_data = ''
    agents = all_agent_data_str.split('\n')
    for agent_str in agents:
        if agent_str:
            agent_info = agent_str.split()
            agent_id = agent_info[0]
            serial_number = agent_info[1]
            path = ' '.join(agent_info[3:])
            formatted_data += f'Agent {agent_id} {serial_number} {path}\n'
    return formatted_data.strip()

def add_intermediate_positions(agent):
    new_list=[]
    first_point=agent["path"][0]
    if len(agent["path"])>2:
        for i in range(1,(agent["path"][3]-agent["path"][1])):
            new_list.append(first_point)
            new_list.append(i)
    else:
        new_list=agent["path"]
    return new_list

def convert_position(path):
    converted_path = []
    for i in range(0, len(path)):
        if isinstance(path[i], tuple):
            x = path[i][1]
            y = path[i][0]
            converted_path.append((x, y))
        else:
            converted_path.append(path[i])
    return converted_path


# Initialize the agent_data list
agent_data = []

# Define the time step duration in minutes
time_step_duration = 5
e_time= time.time()

execution_time = e_time - s_time
print(f"Execution time: {execution_time} seconds")



# Iterate over the agents
for agent in agents:
    agent["path"] = agent["path"][:2]+add_intermediate_positions(agent)+agent["path"][2:]
    #agent["path"] = convert_path(agent["path"])
    agent["path"] = convert_position(agent["path"])
    # Initialize agent-specific data
    agent_path = agent["path"]
    agent_id = agent["serial_number"]
    agent_steps = []
    print("agent path--------------------------------", agent["serial_number"], agent["path"])

    # Iterate over the agent's path
    for i in range(0, len(agent_path), 2):
        position = agent_path[i]
        timestamp = int(agent_path[i+1])

        # Extract x and y coordinates from the position tuple
        x, y = position

        # Calculate the time step based on the timestamp
        # time_step = int(timestamp.minute // time_step_duration + timestamp.hour * 60 // time_step_duration)

        # Create a string representing the agent step
        agent_step = f"{x} {y} {timestamp}"

        # Append the agent_step string to the agent_steps list
        agent_steps.append(agent_step)

    # Convert agent_steps to a single string
    agent_steps_str = " ".join(agent_steps)

    # Create the agent_data string for the current agent
    agent_data_str = f"Agent {agent_id} {agent_steps_str}"

    # Append the agent_data string to the agent_data list
    agent_data.append(agent_data_str)

# Create a DataFrame
# Create a dictionary of agent paths
#data = {f"List{i+1}": [coord for sublist in zip_longest(*[agent["path"] for agent in agents], fillvalue=None) for coord in sublist] for i, _ in enumerate(agents)}
data = {f"List{i+1}": path for i, path in enumerate(zip(*[agent["path"] for agent in agents]))}
# Create a DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
#df.to_excel('output11.xlsx', index=False)


# Set up the window and display the animation
WINDOW_WIDTH = 575  # Adjust the window width to your preference
WINDOW_HEIGHT = 640  # Adjust the window height to your preference
WIDTH = 640
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Convert the agent_data list to a single string
#all_agent_data_str = "\n".join(agent_data)
#all_agent_data_str = all_agent_data_str.split('\n')
print("--------------------------------------------")
print(agent_data)
#formatted_data = format_agent_data(all_agent_data_str)
Animation.main(WIN, WIDTH, csv_file, [agent_data])




k=1
'''
# Initialize the agent_data list
agent_data = []
# Define the time step duration in minutes
time_step_duration = 5

# Iterate over the agent's path
for i in range(0, len(agent["path"]), 2):
    position = agent["path"][i]
    timestamp = int(agent["path"][i+1])

    # Extract x and y coordinates from the position tuple
    x, y = position

    # Calculate the time step based on the timestamp
   # time_step = int(timestamp.minute// time_step_duration + timestamp.hour*60/time_step_duration)

    # Create a string representing the agent step
    agent_step = f"{x} {y} {timestamp}"

    # Append the agent_step string to the agent_data list
    agent_data.append(agent_step)

# Convert agent_data to a single string
agent_data_str = "Agent 0 " + " ".join(agent_data)

# Store the agent_data string in the desired format
agent_data = [agent_data_str]

WINDOW_WIDTH = 575  # Adjust the window width to your preference 575
WINDOW_HEIGHT = 640  # Adjust the window height to your preference 640
WIDTH = 640
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

Animation.main(WIN, WIDTH, csv_file, agent_data)
'''
