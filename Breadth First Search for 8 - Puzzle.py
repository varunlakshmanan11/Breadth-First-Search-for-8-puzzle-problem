import numpy as np
from queue import Queue

node_initial = [[2,5,8],[1,0,4],[7,3,6]] # Initializing Initial Node as a 2D list
node_goal = [[1,2,3],[4,5,6],[7,8,0]] # Initializing Goal Node as a 2D list

# Defining function to locate the blank space within the given node.
def blank_space(node):
    for i in range(len(node)):
        for j in range(len(node[i])):
            if node[i][j] == 0:
                return i, j
    return None

## Defining set of functions to move the blank tile in different possible directions.
# Function for moving the tile in upward direction.
def up_movement(node):
    x, y = blank_space(node)
    if x == 0: # when this condition is satisfied the blank tile cannot move upward.
        return None
    else:
        node[x][y], node[x - 1][y] = node[x - 1][y], node[x][y] # Swapping the blank tile with the tile above it.
        
    return (node)

# Function for moving the tile in downward direction.
def down_movement(node):
    x,y = blank_space(node) 
    if x == 2: # when this condition is satisfied the blank tile cannot move downward.
        return None
    else:
        node[x][y], node[x + 1][y] = node[x + 1][y], node[x][y] # Swapping the blank tile with the tile below it.
        
    return (node)

# Function for moving the tile towards left.        
def left_movement(node):
    x, y = blank_space(node)
    if y == 0: # when this condition is satisfied the blank tile cannot move left.
        return None
    else:
        node[x][y],node[x][y - 1] = node[x][y - 1], node[x][y] # Swapping the blank tile with the tile to the left of it.
    
    return (node)

# Function for moving the tile towards right.
def right_movement(node):
    x, y = blank_space(node)
    if y == 2: # when this condition is satisfied the blank tile cannot move right.
        return None
    else:
        node[x][y], node[x][y + 1] = node[x][y + 1],  node[x][y] # Swapping the blank tile with the tile to the right of it.
    
    return (node)

# Defining Function for getting possible nodes after each move of the blank tile using the movement functions.
def possible_nodes(node, blank_space):
    possible_states = [] # Creating a empty list to add attained states after each move.
    
    # Adding the state to possible_states when moving up.
    if blank_space(node)[0] > 0:
        up_state = up_movement([row[:] for row in node])
        possible_states.append(up_state)  
    # Adding the state to possible_states when the moving down.
    if  blank_space(node)[0] < 2:
        down_state = down_movement([row[:]for row in node])  
        possible_states.append(down_state)
    # Adding the state to possible_states when moving left.
    if blank_space(node)[1] > 0:
        left_state = left_movement([row[:] for row in node])
        possible_states.append(left_state)
    # Adding the state to possible_states when moving right.
    if blank_space(node)[1] < 2:
        right_state = right_movement([row[:] for row in node])
        possible_states.append(right_state)
    
    # Returning the possible states after adding every moves possible
    return possible_states

# Implementing Breath First Search Algorithm to iterate through every possible nodes to get a feasible and shortest solution.
def BFS(node_initial, node_goal):
    visited = set() # Creating a set to keep track of the nodes visited.
    parent = {} # Creating a empty dictionary to store the parent nodes.
    queue = Queue() # Setting up a empty queue to store the node to be visited.
    queue.put(tuple(map(tuple, node_initial))) # Adding the initial node to the queue.
    node_index = {} # Creating a empty dictionary to store the index of the nodes.
    node_count = 0 # Initializing Node count.
    nodes_info = [] # Creating a empty list to store the node information.
    
    while not queue.empty(): # Checking whether the queue is empty.
        # Taking the first node from queue, which is the initial node and assigning it to current_node.
        current_node = queue.get() 
        # Checking whether current_node is equal to goal node.
        if current_node == tuple(map(tuple,node_goal)): 
        # Returning the path by call the backtracking function, parent node and node_info if current node is equal to goal node.    
            return BFS_Backtracking(parent, current_node, node_initial), parent, nodes_info 
        # Checking whether the current node is in the node_index.
        if current_node not in node_index:
            node_index[current_node] = node_count # Current node is added to the node index for each iteration.
            node_count +=1
        # Adding current node to the visited set.
        visited.add(tuple(map(tuple, current_node)))
        # Assigning a variable to access the possible nodes.
        possible_states = possible_nodes(list(map(list,current_node)), blank_space)
        # For Loop for iterating through each possible state and adding those states to the visited set and parent dictionary.
        for new_state in possible_states:
            if tuple(map(tuple,new_state)) not in visited:
                visited.add(tuple(map(tuple, new_state)))
                parent[tuple(map(tuple, new_state))] = current_node
                queue.put(tuple(map(tuple, new_state))) # Possible states to be visited are added to queue. 
                nodes_info.append((node_index[current_node], node_count, new_state)) # Adding the possible state to the nodes_info list. 
                node_index[tuple(map(tuple, new_state))] = node_count # Adding the possible state to node_index.
                node_count +=1
    return None

# Defining a function for generating path using backtracking to find the path from the goal node to initial node.
def BFS_Backtracking(parent, goal_node, initial_node):
     path = [list(map(list, goal_node))]
     while goal_node != tuple(map(tuple, initial_node)) :
        path.append(parent[tuple(map(tuple, goal_node))])
        goal_node = parent[tuple(map(tuple,goal_node ))]
     path.reverse()
     return path

# Getting final_path, nodes visited and nodes_info from the BFS function.
final_path, visited_nodes, nodes_info = BFS(node_initial, node_goal)

if final_path: # Condition to check whether the final_path is attained.
    step_count = 1  # Initializing the step count.
    for step in final_path: # iterating through each step. 
        print(f"Step {step_count}:") 
        print(np.matrix(step))  # Print the current step's state as a matrix.
        step_count += 1  
else:
    print("No path found.") 

## Defining functions to write the output to text files.
# Defining function to write the information of each node explored with its index and the parent index.
def writing_node_info(nodes_info):
    with open('Nodes_info.txt','w') as f: 
        f.write('node_index\tparent_node_index\tnode\n') 
        for index,(node_count, parent_index, node) in enumerate(nodes_info): # Iterating over the index of node count, parent node and node in nodes_info.
            flattened_node = ' '.join(map(str, np.array(node).flatten())) # Converting the 2D array of the node to 1D array and string.
            f.write(f'      {node_count}             {parent_index}       {flattened_node}\n') # writing the node index, parent node index and node to Nodes_info.txt.
# Defining function to write the visited nodes.
def writing_visited_nodes(visited_nodes):
    with open('Nodes.txt','w') as f:
        for node in visited_nodes: # Iterating over each nodes in visited nodes.
            flattened_visited_node = ' '.join(map(str, np.array(node).flatten())) # Converting the 2D array of the node to 1D array and string.
            f.write(flattened_visited_node + '\n') # Writing the visited nodes to Nodes.txt.
# Defining function to write the final path.
def writing_final_path(final_path):
    with open('nodePath.txt','w') as f:
        for node in final_path: # Iterating over each node in the final path.
            node_transpose = np.array(node).T # Converting the rows in the nodes to columns and vice versa.
            flattened_node = ' '.join(map(str, np.array(node_transpose).flatten())) # Converting the 2D array of the node to 1D array and string.
            f.write(flattened_node + '\n') # Writing the path to nodePath.txt for visualizing in the pygame.

# Calling the defined functions for writing outputs.
writing_node_info(nodes_info)
writing_visited_nodes(visited_nodes)
writing_final_path(final_path)
