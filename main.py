#!/usr/bin/env python

import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to the scenario XML file")
parser.add_argument("-r", "--resolution", default=0.4, type=float)
args = parser.parse_args()

scene_name = args.path.split('/')[-1][:-4] 
cwd = os.getcwd()
input_dir = cwd + "/example/{}.xml".format(scene_name)
output_dir = cwd + "/output/" + scene_name 

print("input_dir: ", input_dir)
print("output_dir: ", output_dir)

os.chdir("MengeFileGenerator")
os.system("python3 menge_generator.py {} -o {} -r {}".format(
    input_dir, output_dir, args.resolution
))
os.chdir(cwd)

os.system("python3 world_generator.py --scene_name {} --plugin".format(
    scene_name
))

# os.system("cp -r ./output/{0} ~/menge_ws/Menge/examples/scene".format(scene_name))
# os.system("cp ./output/{0}/{0}.world ~/menge_ws/src/menge_gazebo/menge_gazebo_worlds/worlds/{0}.world".format(scene_name))




