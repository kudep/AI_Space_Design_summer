#!/bin/bash
cd scene_graph
python -m venv venv
source venv/bin/activate
python script.py
cd ..
cp -f scene_graph/output.json rendering/input.json
cd rendering
python -m venv venv
source venv/bin/activate
python script1.py