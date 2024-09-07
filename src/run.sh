#!/bin/bash
cd scene_graph
source venv/bin/activate
python create_sg.py
cd ..
cp -f scene_graph/output.json rendering/input.json
cd rendering
source venv/bin/activate
python place_in_blender.py