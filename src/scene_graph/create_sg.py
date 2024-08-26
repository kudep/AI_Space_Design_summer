from IDesign import IDesign
from utils import get_text_description,count_interior_items,get_room_dimensions ,output_scene_graph
import os
input("1")
FILE_PATH = input("Enter the file path: ")
input("2")
output_scenegraph_path = os.path.join("data", "output_scene_graph.json")

number_of_objects = count_interior_items(FILE_PATH)
room_dimensions = get_room_dimensions(FILE_PATH)
src_file = "scene_graph.json"
dst_dir = "data"
#number_of_objects = 10
i_design = IDesign(no_of_objects = number_of_objects, 
                  user_input = get_text_description(FILE_PATH), 
                  room_dimensions = room_dimensions,)
    #TODO : Adjust visualization window size according to the room size
# Interior Designer, Interior Architect and Engineer 
i_design.create_initial_design()
# Layout Corrector
i_design.correct_design()
# Layout Refiner
i_design.refine_design()
# Backtracking Algorithm
i_design.create_object_clusters(verbose=False)
#save(self=i_design)
#load(i_design)

i_design.backtrack(verbose=True)

i_design.to_json()
if not os.path.exists(output_scenegraph_path):
    output_scene_graph(src_file, dst_dir)