#!/bin/bash
cd scene_graph
python -m venv venv
source venv/bin/activate
python create_sg.py
cd ..
cp -f scene_graph/output.json rendering/input.json
