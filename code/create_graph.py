import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import pairwise
from datetime import timedelta
import csv
import math

#i<len(PathWithTime)-1 and j<len(agent["path"])-1 and

def collisde_check(agents, PathWithTime):
    for agent in agents:
        for i in range(1, len(PathWithTime),2):
            for j in range(1, len(agent["path"]),2):
                if(agent["path"][j]==PathWithTime[i] and agent["path"][j-1]==PathWithTime[i-1] and agent["path"][j-1]!=(0,8) ):
                    return True , i-1 , None 
                elif PathWithTime[i] not in agent["path"]:
                    nodeofagent= get_location_at_time(agent["path"], PathWithTime[i])
                    if nodeofagent==PathWithTime[i-1]:
                        return True , i-1 , None
                elif  i<len(PathWithTime)-1 and j<len(agent["path"])-1 and PathWithTime[i+1]==agent["path"][j-1] and PathWithTime[i-1]==agent["path"][j+1]:
                       return True, i-1 ,math.inf
    return False , None ,None 



def get_location_at_time(agent_path, desired_time):
    if desired_time not in agent_path:
        closest_value = min(agent_path[1::2], key=lambda x: abs(x - desired_time))
        index = agent_path.index(closest_value)
        node=agent_path[index-1]
    return node  # Return the last known location

def find_path_with_collisions(G, start, goal, start_time, other_agents,agentfortask, pathfound, collide_index, swap):
    
    new_path=[]
    new_path.extend(pathfound[:collide_index])
    
    if swap ==math.inf:
        first_node=pathfound[collide_index]
        second_node=pathfound[collide_index+2]
        '''
        if first_node[0]==first_node[1]and (first_node[1]==9 or first_node[1]==5 or first_node[1]==1):
            temp_node=first_node=pathfound[collide_index+2]
            if first_node[0]==temp_node[0]:
                second_node=(second_node[0] -1, second_node[1])
            else:
                second_node=(second_node[0], second_node[1]+1)
        
        elif first_node[0]==first_node[1]and (first_node[1]==8 or first_node[1]==4 or first_node[1]==0):
            temp_node=first_node=pathfound[collide_index+2]
            if first_node[0]==temp_node[0]:
                second_node=(second_node[0] + 1, second_node[1])
            else:
                second_node=(second_node[0], second_node[1]+1)
        '''
        if first_node[0]==second_node[0] and first_node!=goal and (second_node[0]==0 or second_node[0]==4 or second_node[0]==8):
            second_node=(second_node[0] + 1, second_node[1])
        elif first_node[0]==second_node[0] and first_node!=goal and (second_node[0]==1 or second_node[0]==5 or second_node[0]==9):
            second_node=(second_node[0] -1, second_node[1])
        elif first_node[1]==second_node[1] and first_node[1] !=8:
            second_node=(second_node[0], second_node[1]+1)
        else:
            second_node=(second_node[0], second_node[1]-1)

        if len(new_path)>0:
            new_path.insert(collide_index, second_node)
            new_path.insert(collide_index+1, new_path[collide_index-1]+1 )
        else:
            new_path.insert(collide_index, second_node)
            new_path.insert(collide_index+1, agentfortask["path"][-1]+1 )
        path=nx.astar_path(G, new_path[-2], goal, heuristic=lambda u, v: abs(u[0] - v[0]) + abs(u[1] - v[1]))
        for i in range(1,len(path)):
            new_path.append(path[i])
            new_path.append(new_path[-2]+1)

    else:
            
        if len(new_path)>0:
            neighbors = list(G.neighbors(new_path[-2]))
        else:
            neighbors = list(G.neighbors(agentfortask["path"][-2]))
        collide_time=pathfound[collide_index+1]
        agent_positions=[]
        for agent in other_agents:
            if collide_time in agent["path"]:
                index=agent["path"].index(collide_time)
                agent_positions.append(agent["path"][index-1])
            else:
                agent_positions.append(get_location_at_time(agent["path"], collide_time))

        non_occupied_neighbors = [neighbor for neighbor in neighbors if neighbor not in agent_positions]
        min_distance=10000000
        for neighbor in non_occupied_neighbors:
            distance = abs(neighbor[0]-goal[0])+abs(neighbor[1]-goal[1])
            if distance < min_distance:
                min_distance = distance
                min_neighbor = neighbor 
        
        new_path.append(min_neighbor)
        new_path.append(collide_time)
        path=nx.astar_path(G, min_neighbor, goal, heuristic=lambda u, v: abs(u[0] - v[0]) + abs(u[1] - v[1]))
        for i in range(1,len(path)):
            new_path.append(path[i])
            new_path.append(new_path[-2]+1)
    return new_path
    '''
    temp_neighbors = []
    while new_path[-2] != goal:
        temp_neighbors.append(min_neighbor)
        neighbors = list(G.neighbors(new_path[-2]))
        agent_positions=[]
        for agent in other_agents:
            if new_path[-1]+1 in agent["path"]:
                index=agent["path"].index(new_path[-1]+1)
                agent_positions.append(agent["path"][index-1])
            else:
                agent_positions.append(get_location_at_time(agent["path"], new_path[-1]+1))
        
        non_occupied_neighbors = [neighbor for neighbor in neighbors if neighbor not in agent_positions]
        for i in range(0, len(new_path), 2):
            if new_path[i] in non_occupied_neighbors:
                non_occupied_neighbors.remove(new_path[i])
        if len(non_occupied_neighbors)==0:
            non_occupied_neighbors.append(new_path[-2])
        min_distance =1000000
        for neighbor in non_occupied_neighbors:
            distance = abs(neighbor[0]-goal[0])+abs(neighbor[1]-goal[1])
            if distance < min_distance:
                min_distance = distance
                min_neighbor = neighbor 
         
        new_path.append(min_neighbor)
        new_path.append(new_path[-2]+1)
    
    return new_path
'''

class graph:

    def create_graph_from_csv(csv_file, delimiter=','):
        # Read CSV file and extract grid data
        grid_data = []
        names={}
        with open(csv_file, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            for i, row in enumerate(reader):
                grid_data.append(row)
                for j, name in enumerate(row):
                    if name[0]=='A' or name[0]=='B' or name[0]=='C':
                        names[(i-1, j)] = name
        print(names)  # Print names dictionary for debugging

        # Determine the number of rows and columns
        num_rows = len(grid_data)
        num_cols = len(grid_data[0])

        # Create a 2D grid graph
        G = nx.grid_2d_graph(num_rows, num_cols)

        # Remove obstacle nodes from the graph
        for i in range(num_rows):
            for j in range(num_cols):
                if grid_data[i][j] == '1':
                    G.remove_node((i, j))
        
        copy_graph=G.copy()
        for node in copy_graph.nodes():
            x, y = node
            new_node = (x - 1, y)
            G = nx.relabel_nodes(G, {node: new_node}, copy=False)

        # Create a dictionary of node positions
        pos = {(i, j): (j, i-1) for i in range(num_rows) for j in range(num_cols)}

        pos.update({(-1, 0): (0,-1), (-1, 1): (1, -1), (-1, 2): (2, -1), (-1, 3): (3, -1)})

                # Assign weights to the edges
        for u, v in G.edges():
            G[u][v]['weight'] = abs(u[0] - v[0]) + abs(u[1] - v[1])  # Manhattan distance
        
        
        #nx.draw(G, pos=pos, labels=names, with_labels=True, node_size=500, font_size=8, font_weight='bold')
        #Add position labels to each node
        #nx.draw_networkx_labels(G, pos, labels=pos)
        #plt.show()

        return G, names, pos


    def create_graph(row, column):
        row=9
        column=10
        G = nx.grid_2d_graph(row, column)

        # Create a dictionary of node positions
        pos = {node: node for node in G.nodes()}



        G.remove_nodes_from([(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),
                            (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),
                            (0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),
                            (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),
                            (0,0),(1,0),(2,0),(3,0),(4,0),(5,0)])

        names = {}
        for i, j in G.nodes():
            if i in range(1, 7):
                if j == 1:
                    names[(i, j)] = f'A{i}0'
                elif j == 5:
                    names[(i, j)] = f'B{i}0'
                elif j == 9:
                    names[(i, j)] = f'C{i}0'
                    
            
            
        nx.set_node_attributes(G, names, 'name')
        G.add_nodes_from([(0, 0), (1, 0), (2, 0), (3,0)])
        MoreEdges= [((7,1),(7,4)), ((8,1),(8,4)), ((7,5),(7,8)), ((8,5),(8,8)), ((0,1),(0,4)), ((0,5),(0,8))]
        agent_edeges=[((0,0),(0,1)), ((1,0), (1,1)),((2,0),(2,1)),((3,0),(3,1))]

        G.add_edges_from(MoreEdges)
        G.add_edges_from(agent_edeges)
        # Assign weights to the edges
        for u, v in G.edges():
            G[u][v]['weight'] = abs(u[0] - v[0]) + abs(u[1] - v[1])  # Manhattan distance

        #nx.draw(G, pos=pos, labels=names, with_labels=True, node_size=500, font_size=8, font_weight='bold')
        #plt.show()
        return G, names, pos
    

    
    def get_key_from_value(names, value):
        return next((key for key, val in names.items() if val == value), None)
    
    def manhattan_distance (package_loacation, agent_loacation):
        distance = abs(package_loacation[0] - agent_loacation[0]) + abs(package_loacation[1] - agent_loacation[1]) 
        return distance
    
    def find_path(G, names, pos, agents,agentfortask, start, goal, start_time):
        # Perform heuristic search between the specified nodes
        path = nx.astar_path(G, start, goal, heuristic=lambda u, v: abs(u[0] - v[0]) + abs(u[1] - v[1]))

        # Calculate the cost of the path
        cost = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))

        # Update the agent's path
        delta_t = 5  # Set the time increment
        current_time = start_time
        previous_point = start  # Store the previous point
        PathWithTime=[]
        for point in path:
            agentfortask["des_location"]["location"] = point
            edge_data = G.get_edge_data(previous_point, point)
            PathWithTime.append(point)
            if edge_data is not None:
                agentfortask["des_location"]["time"] = current_time + delta_t * timedelta(minutes=edge_data['weight'])
                time = current_time + delta_t * timedelta(minutes=edge_data['weight'])
                time_step = int(time.minute // delta_t + time.hour * 60 / delta_t)
                PathWithTime.append(int(time_step))
            else:
                agentfortask["des_location"]["time"] = current_time
                PathWithTime.append(int(current_time.minute // delta_t + current_time.hour * 60 / delta_t))
            current_time = agentfortask["des_location"]["time"]
            previous_point = point  # Update the previous point

        # Check for collisions with other agents
        #colliding_agents = []
        #for agent in agents:
        #    if len(agent["path"])>0 and agent["serial_number"]!=agentfortask["serial_number"]:
         #       for i in range(1, len(PathWithTime),2):
          #          for j in range(1, len(agent["path"]),2):
           #             if(agent["path"][j]==PathWithTime[i] and agent["path"][j-1]==PathWithTime[i-1]):
            #                colliding_agents.append(agent)  
             #           elif PathWithTime[i] not in agent["path"]:
              #              nodeofagent= get_location_at_time(agent["path"], PathWithTime[i])
               #             if nodeofagent==PathWithTime[i-1]:
                #                colliding_agents.append(agent)  
        collide, collide_index, swap = collisde_check(agents[:agentfortask["serial_number"]-1] + agents[agentfortask["serial_number"]:], PathWithTime)
        if collide==True:
            time_steps_start_time= int(start_time.minute // delta_t + start_time.hour * 60 / delta_t)
            indexofagent=agentfortask["serial_number"]
            agentlist=agents[:indexofagent-1] + agents[indexofagent:]
            pathwithnocollide= find_path_with_collisions(G, start, goal, time_steps_start_time, agentlist,agentfortask,PathWithTime, collide_index, swap)
            PathWithTime=pathwithnocollide

        agentfortask["path"].extend(PathWithTime)
            # Draw the graph with the agent's movement
        for i in range(len(path) - 1):
            current_pos = path[i]
            next_pos = path[i + 1]
            # Update the agent's location
            agentfortask["des_location"]["location"] = next_pos

            if agentfortask["serial_number"]==0:
                color='red'
            elif agentfortask["serial_number"]==1:
                color='green'
            elif agentfortask["serial_number"]==2:
                color='blue'
            else:
                color='yellow'

            # Highlight the nodes and edges for the agent's movement
            nx.draw_networkx_nodes(G, pos=pos, nodelist=[current_pos], node_color='blue', node_size=500)
            nx.draw_networkx_nodes(G, pos=pos, nodelist=[next_pos], node_color='red', node_size=500)
            nx.draw_networkx_edges(G, pos=pos, edgelist=[(current_pos, next_pos)], edge_color=color, width=3)

        # Draw the graph with labels and other nodes
        nx.draw(G, pos=pos, labels=names, with_labels=True, node_size=500, font_size=8, font_weight='bold')

        # Add edge labels
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_color='red')
        #plt.show()

            # Update the agent's location
        #agent["des_location"]["location"] = next_pos

        return agentfortask
    




'''
    def find_path(G, names, pos, agent, start, goal, start_time):
        # Perform heuristic search between the specified nodes
        path = nx.astar_path(G, start, goal, heuristic=lambda u, v: abs(u[0] - v[0]) + abs(u[1] - v[1]))

        # Calculate the cost of the path
        cost = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))

        # Update the agent's path
        #agent["path"].extend(path)

        # Update the agent's location and time based on the path and cost
        delta_t = 5  # Set the time increment
        current_time = start_time
        previous_point = start  # Store the previous point
        for point in path:
            agent["des_location"]["location"] = point
            edge_data = G.get_edge_data(previous_point, point)
            agent["path"].append(point)
            if edge_data is not None:
                agent["des_location"]["time"] = current_time + delta_t * timedelta(minutes= edge_data['weight'])
                time=current_time + delta_t * timedelta(minutes= edge_data['weight'])
                time_step=int(time.minute// delta_t + time.hour*60/delta_t)
                agent["path"].append(time_step)
            else:
                agent["des_location"]["time"] = current_time
                agent["path"].append(current_time.minute// delta_t + current_time.hour*60/delta_t)
            current_time = agent["des_location"]["time"]
            previous_point = point  # Update the previous point

        # Draw the graph with the agent's movement
        for i in range(len(path) - 1):
            current_pos = path[i]
            next_pos = path[i + 1]

            # Update the agent's location
            agent["des_location"]["location"] = next_pos

            # Highlight the nodes and edges for the agent's movement
            #nx.draw_networkx_nodes(G, pos=pos, nodelist=[current_pos], node_color='blue', node_size=500)
            #nx.draw_networkx_nodes(G, pos=pos, nodelist=[next_pos], node_color='red', node_size=500)
            #nx.draw_networkx_edges(G, pos=pos, edgelist=[(current_pos, next_pos)], edge_color='green', width=3)

        # Draw the graph with labels and other nodes
        #nx.draw(G, pos=pos, labels=names, with_labels=True, node_size=500, font_size=8, font_weight='bold')

        # Add edge labels
        #edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        #nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_color='red')
        #plt.show()

        return agent
'''





'''
    def find_path(G, names, pos, agent, start, goal):
        # Iterate over the agents
        #for agent in agents:
         #   start_node = agent["des_location"]["location"]  # Get the start node based on the agent's location
          #  goal_node = graph.get_key_from_value(names, 'A10')  # Replace with your desired goal node

            #start = next((n for n, d in G.nodes(data=True) if n == start_node), None)
            #goal = next((n for n, d in G.nodes(data=True) if n == goal_node), None)

            # Perform heuristic search between the specified nodes
            path = nx.astar_path(G, start, goal, heuristic=lambda u, v: abs(u[0] - v[0]) + abs(u[1] - v[1]))

            # Update the agent's path
            agent["path"] = path

            # Draw the graph with the agent's movement
            for i in range(len(path) - 1):
                current_pos = path[i]
                next_pos = path[i + 1]

                # Update the agent's location
                agent["des_location"] = next_pos


            # Draw the graph with labels and other nodes
            nx.draw(G, pos=pos, labels=names, with_labels=True, node_size=500, font_size=8, font_weight='bold')

            # Add edge labels
            edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
            nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_color='red')
            plt.show()



    def find_path(G, names, pos):
        # Specify the nodes you want to search between by name
        start_node = 'A10'
        goal_node = 'C50'

        # Find the nodes corresponding to the specified names
        start = next((n for n, d in G.nodes(data=True) if d.get('name') == start_node), None)
        goal = next((n for n, d in G.nodes(data=True) if d.get('name') == goal_node), None)

        # Perform heuristic search between the specified nodes
        path = nx.astar_path(G, start, goal, heuristic=lambda u, v: abs(u[0] - v[0]) + abs(u[1] - v[1]))

        # Highlight the nodes and edges on the search path
        search_path_edges = list(pairwise(path))
        search_path_nodes = path + [start, goal]
        nx.draw_networkx_edges(G, pos=pos, edgelist=search_path_edges, edge_color='red', width=3)
        nx.draw_networkx_nodes(G, pos=pos, nodelist=search_path_nodes, node_color='red', node_size=500)

        # Draw the graph
        nx.draw(G, pos=pos,labels=names, with_labels=True, node_size=500, font_size=8, font_weight='bold')

        # Add edge labels
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_color='red')

        plt.show()
'''


   