from room import Room
from player import Player
from world import World
from traversal_graph import Graph
from util import Queue, Stack

import random
from ast import literal_eval

# Load world 
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# We create a list for tracking the movements we need to make to get back to the list room with question marks
backtracking_path = []

traversal_graph = {
    '0': {'n': '?', 's': '?', 'w': '?', 'e': '?', }
}
room_ids = set()
move_counter = 0
roll_counter = 0

compass_dict = {'1': 'n', '2': 's', '3': 'w', '4': 'e'}
reverse_num_compass = {'1': 's', '2': 'n', '3': 'e', '4': 'w'}
reverse_compass = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

# We create a queue with the starting room at the front of the queue
qq = Queue()

# We roll the dice to determine which direction we will move in first
random_number = random.randint(1, 4)
roll_counter += 1
first_move = compass_dict[str(random_number)]

# We enqueue the first move
qq.enqueue([first_move])

# Pick a random direction to move in
# for i in range(2000):
# We use a while loop that runs as long as there are unexplored rooms
# while len(room_ids) < 500:
while move_counter < 10:
# while qq.size() > 0:
    # We dequeue the room at the front of the queue
    current_path = qq.dequeue()
    move = current_path[-1]
    reverse_move = reverse_compass[move]
    
    # We create a variable to track the room we're in and add it to the list of rooms we've visited
    starting_room = player.current_room.id
    room_ids.add(starting_room)
    print("Current room: ", starting_room)
    print("Next move: ", move)
    print("Reverse move: ", reverse_move)
    # print("This is len(room ids): ", len(room_ids))
    # print("This is move: ", move)

    # random_number = random.randint(1, 4)
    # roll_counter += 1
    # move = compass_dict[str(random_number)]
    # reverse_move = reverse_num_compass[str(random_number)]


    # We check to see if the direction the player wants to move in is available
    if player.current_room.get_room_in_direction(move) != None:
        # If so, we use player.travel() to move the player in the desired direction
        player.travel(move)
        # Then we append that move to the traversal path and increment the move counter by 1
        traversal_path.append(move)
        move_counter += 1

        # We create a variable to represent the room the player just moved to
        new_room = player.current_room.id


        # Update traversal graph for room we left by pointing to the new room in the correct direction
        traversal_graph[str(starting_room)][move] = new_room
        print("Trav graph update: ", traversal_graph[str(starting_room)])

        # We check to see if the room we just moved to is in our traversal graph
        if new_room in traversal_graph:
            # If it is, we update the direction we came from to point to the room we just left
            traversal_graph[str(new_room)][reverse_move] = starting_room
            # print("Trav graph backtrack update: ", traversal_graph[str(starting_room)])
            print("Trav graph backtrack update: ", traversal_graph[str(starting_room)])

        # Otherwise, we assume the new room is not in the dictionary
        else: 
            # And create a dictionary entry for it before updating the direction we came from to point to the room we just left
            traversal_graph[str(new_room)] = {'n': '?', 's': '?', 'w': '?', 'e': '?', }
            traversal_graph[str(new_room)][reverse_move] = starting_room
            # print("Trav graph backtrack update: ", traversal_graph[str(starting_room)])
            print("Trav graph backtrack update: ", traversal_graph[str(starting_room)])
    
    # If the desired movement is not available, we update that direction of the room to None
    else:
        traversal_graph[str(starting_room)][move] = None
    

    exits = player.current_room.get_exits()
    print("Room before new path calc: ", new_room)

    # We use a for loop to loop through the available exits of the room we're in
    for direction in exits:
        # If a room only has one exit, we just append that direction to the new path before enqueuing it
        if len(exits) == 1:
            new_path = list(current_path)
            new_path.append(direction)
            print("This is only path: ", new_path)
            qq.enqueue(new_path)
        
        # But if a room has multiple exits, we check one exit at a time to see if it's unexplored, and if it is unexplored, we append that direction to a new path and enqueue it
        elif traversal_graph[str(starting_room)][direction] == '?':
            # print("Trav graph for room: ", traversal_graph[str(starting_room)])
            new_path = list(current_path)
            new_path.append(direction)
            print("This is new path: ", new_path)
            qq.enqueue(new_path)

# print("This is traversal path: ", traversal_path)
print("This is traversal graph: ", traversal_graph)
# print("This is room ids: ", room_ids)
print("This is roll counter: ", roll_counter)
print("This is move counter: ", move_counter)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
