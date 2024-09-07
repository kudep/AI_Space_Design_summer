import bpy
import json
import math
import os

object_name = 'Cube'
object_to_delete = bpy.data.objects.get(object_name)


# Check if the object exists before trying to delete it
if object_to_delete is not None:
    bpy.data.objects.remove(object_to_delete, do_unlink=True)
    
def import_glb(file_path, object_name):
       bpy.ops.import_scene.gltf(filepath=file_path)
       imported_object = bpy.context.view_layer.objects.active
       if imported_object is not None:
           imported_object.name = object_name

def create_room(width, depth, height):
    # Create floor
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))

    # Extrude to create walls
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, height)})
    bpy.ops.object.mode_set(mode='OBJECT')

    # Scale the walls to the desired dimensions
    bpy.ops.transform.resize(value=(width, depth, 1))

    bpy.context.active_object.location.x += width / 2
    bpy.context.active_object.location.y += depth / 2

def find_glb_files(directory):
    glb_files = {}
    print(f"Search.glb files in the directory: {directory}")
    
    for root, dirs, files in os.walk(directory):
        print(f"\nCurrent directory: {root}")
        print("Subdirectories:", dirs)
        print("files", files)
        
        for file in files:
            if file.endswith(".glb"):
                key = file.split(".")[0]
                if key not in glb_files:
                    full_path = os.path.join(root, file)
                    glb_files[key] = full_path
                    print(f"Found .glb file: {file} (The full path: {full_path})")
    
    print(f"\nTotal found .glb files: {len(glb_files)}")
    return glb_files

def get_highest_parent_objects():
    highest_parent_objects = []

    for obj in bpy.data.objects:
        # Check if the object has no parent
        if obj.parent is None:
            highest_parent_objects.append(obj)
    return highest_parent_objects

def delete_empty_objects():
    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object is empty (has no geometry)
        print(obj.name, obj.type)
        if obj.type == 'EMPTY':
            bpy.context.view_layer.objects.active = obj
            bpy.data.objects.remove(obj)

def select_meshes_under_empty(empty_object_name):
    # Get the empty object
    empty_object = bpy.data.objects.get(empty_object_name)
    print(empty_object is not None)
    if empty_object is not None and empty_object.type == 'EMPTY':
        # Iterate through the children of the empty object
        for child in empty_object.children:
            # Check if the child is a mesh
            if child.type == 'MESH':
                # Select the mesh
                child.select_set(True)
                bpy.context.view_layer.objects.active = child
            else:
                select_meshes_under_empty(child.name)

def rescale_object(obj, scale):
    # Ensure the object has a mesh data
    if obj.type == 'MESH':
        try:
            bbox_dimensions = obj.dimensions
            scale_factors = (
                             scale["length"] / bbox_dimensions.x, 
                             scale["width"] / bbox_dimensions.y, 
                             scale["height"] / bbox_dimensions.z
                            )
            obj.scale = scale_factors
        except Exception as e:
            print(f"An error occurred when changing the scale of the object: {e}")
    else:
        print(f"Error: Object '{obj.name}' This is not a mash. It is impossible to change the scale.")

def hex_to_rgb(value):
    #to work with color
    gamma = 2.2
    value = value.lstrip('#')
    lv = len(value)
    fin = list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r = pow(fin[0] / 255, gamma)
    g = pow(fin[1] / 255, gamma)
    b = pow(fin[2] / 255, gamma)
    fin.clear()
    fin.append(r)
    fin.append(g)
    fin.append(b)
    return tuple(fin)


objects_in_room = {}
file_path = "/home/mnim/AI_Space_Design_summer/src/rendering/input.json" #here you can specify your path
with open(file_path, 'r') as file:
    data = json.load(file)
    for item in data:
        if item["new_object_id"] not in ["south_wall", "north_wall", "east_wall", "west_wall", "middle of the room", "ceiling"]:
            objects_in_room[item["new_object_id"]] = item

directory_path = os.path.join(os.getcwd(), "Assets")
glb_file_paths = find_glb_files(directory_path)

for item_id, object_in_room in objects_in_room.items():
    if item_id in glb_file_paths:
        glb_file_path = os.path.join(directory_path, glb_file_paths[item_id])
        import_glb(glb_file_path, item_id)
    else:
        print(f"Warning: No .glb file found for {item_id}")

parents = get_highest_parent_objects()
empty_parents = [parent for parent in parents if parent.type == "EMPTY"]
print(empty_parents)

for empty_parent in empty_parents:
    bpy.ops.object.select_all(action='DESELECT')
    select_meshes_under_empty(empty_parent.name)
    
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    
    joined_object = bpy.context.view_layer.objects.active
    if joined_object is not None:
        joined_object.name = empty_parent.name + "-joined"

bpy.context.view_layer.objects.active = None

MSH_OBJS = [m for m in bpy.context.scene.objects if m.type == 'MESH']
for OBJS in MSH_OBJS:
    bpy.context.view_layer.objects.active = OBJS
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    OBJS.location = (0.0, 0.0, 0.0)
    bpy.context.view_layer.objects.active = OBJS
    OBJS.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

MSH_OBJS = [m for m in bpy.context.scene.objects if m.type == 'MESH']
for OBJS in MSH_OBJS:
    item = objects_in_room[OBJS.name.split("-")[0]]
    object_position = (item["position"]["x"], item["position"]["y"], item["position"]["z"])  # X, Y, and Z coordinates
    object_rotation_z = (item["rotation"]["z_angle"] / 180.0) * math.pi + math.pi # Rotation angles in radians around the X, Y, and Z axes
    
    bpy.ops.object.select_all(action='DESELECT')
    OBJS.select_set(True)
    OBJS.location = object_position
    bpy.ops.transform.rotate(value=object_rotation_z,  orient_axis='Z')
    rescale_object(OBJS, item["size_in_meters"])

bpy.ops.object.select_all(action='DESELECT')
delete_empty_objects()

room = "/home/mnim/AI_Space_Design_summer/src/rendering/room.json"#here you can specify your path
with open(room, 'r') as j:
    config = json.load(j)
    wid = config["room"]["scale"]["width"]
    dep = config["room"]["scale"]["depth"]
    hei = config["room"]["scale"]["height"]
    
create_room(wid, dep, hei)


config_cameras = config["cameras"]

for cam_obj in config_cameras:
    #reading json to install cameras
    if cam_obj["wall"] == 'x+':
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, hei/2), rotation=(cam_obj["rotation"]["x"]*math.pi/180, cam_obj["rotation"]["y"]*math.pi/180, cam_obj["rotation"]["z"]*math.pi/180), scale=(1, 1, 1))
        bpy.context.object.data.lens = cam_obj["focal_length"]
        bpy.context.scene.cycles.samples = cam_obj["samples"]
    elif cam_obj["wall"] == 'y+':
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(wid, dep, hei/2), rotation=(cam_obj["rotation"]["x"]*math.pi/180, cam_obj["rotation"]["y"]*math.pi/180, cam_obj["rotation"]["z"]*math.pi/180), scale=(1, 1, 1))
        bpy.context.object.data.lens = cam_obj["focal_length"]
        bpy.context.scene.cycles.samples = cam_obj["samples"]
    else:
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', rotation=(cam_obj["rotation"]["x"]*math.pi/180, cam_obj["rotation"]["y"]*math.pi/180, cam_obj["rotation"]["z"]*math.pi/180), scale=(1, 1, 1))
        bpy.context.object.data.lens = cam_obj["focal_length"]
        bpy.context.scene.cycles.samples = cam_obj["samples"]
        
config_l = config["lamps"]
for light in config_l:
    #reading json to install lamps
    if light["number"] == 1:
        bpy.ops.object.light_add(type='AREA', radius=light["radius"], align='WORLD', location=(light["location"]["x"], light["location"]["y"], light["location"]["z"]), scale=(1, 1, 1))
        bpy.context.object.data.color = (hex_to_rgb(light["color"]))        
        bpy.context.object.data.energy = light["power"]
    elif light["number"] == 2:
        bpy.ops.object.light_add(type='AREA', radius=light["radius"], align='WORLD', location=(light["location"]["x"], light["location"]["y"], light["location"]["z"]), scale=(1, 1, 1))
        bpy.context.object.data.color = (hex_to_rgb(light["color"])) 
        bpy.context.object.data.energy = light["power"]
    else:
        bpy.ops.object.light_add(type='AREA', radius=light["radius"], align='WORLD', location=(light["location"]["x"], light["location"]["y"], light["location"]["z"]), scale=(1, 1, 1))
        bpy.context.object.data.color = (hex_to_rgb(light["color"])) 
        bpy.context.object.data.energy = light["power"]
