# IDesign
This is the official Github Repo for [*I-Design: Personalized LLM Interior Designer*](https://atcelen.github.io/I-Design/)

The program receives an input request to create a design in the form of an object of the iDesign class, the object contains information about the number
of interior items in the room, the size of the room, and directly a description of the room from the user. Further, this information is transmitted using fr
amework autogen through a pipeline from LLM (model data comes from the json file OAI_CONFIG_LIST), between which the transfer is carried out in json format, for this
purpose there is a json schema in the file for each LLM schemas.py rendering and creation of the interior in 3D format is carried out using the bpy module, therefore
LLM does not have access to any database of 3D models, but creates them itself using the bpy module.

## Requirements
Install the requirements
```bash
pip install bpy
cd src
cd scene_graph
pip install pyautogen==0.2.0
pip install networkx==2.6.3
pip install jsonschema==4.3.2
pip install matplotlib
pip install pydantic==1.10.2
pip install torch_redstone
pip install einops
pip install huggingface_hub
```
Create the "OAI_CONFIG_LIST.json" file in src/scene_graph
```json
[
    {
        "model": "gpt-4",
        "api_key": "YOUR_API_KEY"
    },
    {
        "model": "gpt-4-1106-preview",
        "api_key": "YOUR_API_KEY"
    },
    {
        "model": "gpt-3.5-turbo-1106",
        "api_key": "YOUR_API_KEY",
        "api_version": "2023-03-01-preview"
    }
]
```

## Inference
Create the "room.json" file in src/scene_graph
```json
{
 "description": ["enumeration of objects"],
 "no_of_objects": ["number of objects"],
 "room_razmery": ["room dimensions"]
}
```
Create the scene graph and allocate coordinate positions
```python
from IDesign import IDesign
from utils import get_text_description,count_interior_items,get_room_dimensions ,output_scene_graph
import os
FILE_PATH = input("Enter the file path: ")
output_scenegraph_path = os.path.join("data", "output_scene_graph.json")

number_of_objects = count_interior_items(FILE_PATH)
room_dimensions = get_room_dimensions(FILE_PATH)


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
    output_scene_graph(os.getenv(src_file), os.getenv(dst_dir))
```

Retrieve the 3D assets from Objaverse using OpenShape
```bash
git clone https://huggingface.co/OpenShape/openshape-demo-support
cd openshape-demo-support
pip install -e .
cd ..
python retrieve.py
```

Place the assets using the Blender Scripting Module using the script in the *place_in_blender.py* file

## Evaluation
After creating scene renders in Blender, you can use the GPT-V evaluator to generate grades for evaluation. Fill in the necessary variables denoted with TODO and run the script
```bash
python gpt_v_as_evaluator.py
```

## Results
![gallery](imgs/gallery.jpg)
