from ai_agent.templates import *
from ai_agent.agent import *
from ai_agent.brain_tree import *
from ai_agent.game_handler import *
from ai_agent.cost_functions import *
from ai_agent.new_cost import *
import time


game = [[3, 28], [4, 28], [3, 29], [4, 29], [5, 28], [6, 28], [5, 29], [6, 29], [7, 25], [6, 26], [7, 26], [6, 27], [1, 27], [1, 28], [2, 28], [2, 29], [3, 25], [3, 26], [4, 26], [3, 27], [1, 24], [1, 25], [2, 25], [1, 26]]
game = [[3, 28], [2,26], [5,26], [4, 28], [3, 29], [4, 29], [5, 28], [6, 28], [5, 29], [6, 29], [7, 25], [6, 26], [7, 26], [8,26],[6, 27], [1, 27], [1, 28], [2, 28], [2, 29], [3, 25], [5,27], [3, 26], [4, 26], [3, 27], [1, 24], [1, 25], [2, 25], [1, 26]]
#piece = array_to_piece([[2, 3], [3, 3], [4, 3], [5, 3]])
game_map = coord_to_bitmap(game)

cost_multipliers = [1, 12.885008263218383, 15.842707182438396, 26.894496507795950, 27.6169140623970150, 30.185110719279040]
corr = [0,31,0,4,6,17]

print_bitmap(game_map|BORDER_BOTTOM)
#print("\ncorrect:")
#print("get_cleaned_rows 0")
#print("get_height_of_block 31")
#print("get_well_cells_number 0")
#print("get_number_of_holes_in_collumns 4")
#print("get_transition_number_in_collumns 6")
#print("get_transition_number_in_rows 17")
#print(sum([ cost_multipliers[i]*corr[i] for i in range( len(corr) ) ] ) ) 

#print("\nold costs:")
#print(get_cost(game_map, cost_multipliers))
#
#print("\nnew costs:")
#print(get_cost_global(game_map, cost_multipliers))
#
#print("\nbroken costs:")
#print(get_cost_broken(game_map, cost_multipliers))

attempts = 10000

#print("\nold costs:")
#start0 = time.time()
#
#for i in range(attempts):
#    get_cost(game_map, cost_multipliers)
#
#end0 = time.time()
#
#print("\n\nresults:")
#print("old: ", end0-start0)
#
#
#print("\nnew costs:")
#start1 = time.time()
#
#for i in range(attempts):
#    get_cost(game_map, cost_multipliers)
#
#end1 = time.time()
#
#print("\n\nresults:")
#print("new: ", end1-start1)
#
#
#print("\nbroken costs:")
#start2 = time.time()
#
#for i in range(attempts):
#    get_cost(game_map, cost_multipliers)
#
#end2 = time.time()
#
#print("\n\nresults:")
#print("broken: ", end2-start2)

st = time.time()
for i in range(attempts):
    generate_base_tree('Z', game_map, cost_multipliers)
print(time.time() -st)
