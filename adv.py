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
traversal_graph = {
    0: {'n': '?', 's': '?', 'w': '?', 'e': '?', }
}
room_ids = set()
move_counter = 0
roll_counter = 0

compass_dict = {'1': 'n', '2': 's', '3': 'w', '4': 'e'}

# Pick a random direction to move in
# for i in range(2000):
while len(room_ids) < 500:
    random_number = random.randint(1, 4)
    roll_counter += 1
    # print("This is random_number: ", random_number)
    move = compass_dict[str(random_number)]
    # print("This is move: ", move)
    # print("This is room id: ", player.current_room.id)
    room_ids.add(player.current_room.id)
    # print("This is room ids: ", room_ids)
    # print("This is len(room ids): ", len(room_ids))

    if getattr(player.current_room, f'{move}_to') != None:
        player.travel(move)
        traversal_path.append(move)
        move_counter += 1
        # print("This is room id: ", player.current_room.id)
        # print("This is traversal_path: ", traversal_path)

print("This is move counter: ", move_counter)
print("This is roll counter: ", roll_counter)
# if random_direction == 1:
#     move = 'n'
#     # Move in that direction
#     player.travel(move)
#     # Log that direction
#     traversal_path.append(move)
#     print("This is traversal_path: ", traversal_path)
# elif random_direction == 2:
#     move = 's'
#     # Move in that direction
#     player.travel(move)
#     # Log that direction
#     traversal_path.append(move)
#     print("This is traversal_path: ", traversal_path)
# elif random_direction == 3:
#     move = 'w'
#     # Move in that direction
#     player.travel(move)
#     # Log that direction
#     traversal_path.append(move)
#     print("This is traversal_path: ", traversal_path)
# elif random_direction == 4:
#     move = 'e'
#     # Move in that direction
#     player.travel(move)
#     # Log that direction
#     traversal_path.append(move)
#     print("This is traversal_path: ", traversal_path)



qq = Queue()
qq.enqueue([player.current_room.id])

available_directions = player.current_room.get_exits()
# print("This is available directions: ", available_directions)




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
