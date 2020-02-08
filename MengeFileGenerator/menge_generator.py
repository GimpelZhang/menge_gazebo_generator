#!/usr/bin/env python

import os
import argparse
import imageio
import scipy.misc
import xml.dom.minidom as xdm
import xml.etree.ElementTree as et

from block_generator import BlockGenerator

WALL_IMAGE = None

SCENE_XML = et.parse('base_scene.xml').getroot()


def write_to_XML(node, fileName):
    data = et.tostring(node)
    data = xdm.parseString(data)
    data = data.toprettyxml(indent="\t")
    outfile = open('%s.xml' % fileName, 'w')
    outfile.write(data)
    outfile.close()


'''
######################## Main Program ######################## 
'''

def main(resolution):

    global WALL_IMAGE
    # global MAIN_XML, BEHAVIOR_IMAGE, WALL_IMAGE, COLOR_DICTIONARY
    # MAIN_XML = et.parse(XML_PATH).getroot()
    # BEHAVIOR_IMAGE = imageio.imread(BEHAVIOR_PNG_PATH)
    WALL_IMAGE = imageio.imread(WALL_PNG_PATH)

    if not os.path.exists("%s/" % OUTPUT_PATH):
        print("Creating output directory './%s/'" % OUTPUT_PATH)
        os.makedirs("%s/" % OUTPUT_PATH)

    # print("Creating link file '%s/%s.xml'..." % (OUTPUT_PATH, SCENARIO_NAME))
    # link_xml = create_XML_link()
    # write_to_XML(link_xml, '%s/%s' % (OUTPUT_PATH, SCENARIO_NAME))

    # print("Creating viewer file '%s/%sV.xml'..." % (OUTPUT_PATH, SCENARIO_NAME))
    #　create_XML_viewer()
    # write_to_XML(VIEWER_XML, '%s/%sV' % (OUTPUT_PATH, SCENARIO_NAME))

    # print("Creating behavior file '%s/%sB.xml..." % (SCENARIO_NAME, SCENARIO_NAME))
    # COLOR_DICTIONARY = create_color_dictionary(BEHAVIOR_IMAGE, resolution=resolution)
    # if not create_XML_scene_behavior():
    #    return
    # write_to_XML(BEHAVIOR_XML, '%s/%sB' % (OUTPUT_PATH, SCENARIO_NAME))

    print("Creating scene file '%s/%sS.xml..." % (SCENARIO_NAME, SCENARIO_NAME))
    # wall_points = square_generator.build_point_dict(WALL_IMAGE, 255)
    # wall_squares = square_generator.build_square_list(WALL_IMAGE, wall_points)
    # data = {
    #     'width': int(WALL_IMAGE.shape[1]),
    #     'height': int(WALL_IMAGE.shape[1]),
    #     'squares': wall_squares
    # }
    # obstacle_set_node = wall_generator.create_obstacle_set(data, resolution=resolution)
    block_generator = BlockGenerator()
    obstacle_set_node = block_generator.generate(WALL_IMAGE, resolution)
    SCENE_XML.append(obstacle_set_node)
    write_to_XML(SCENE_XML, '%s/%sS' % (OUTPUT_PATH, SCENARIO_NAME))

    # print("Creating road map file %s/%s.txt..." % (OUTPUT_PATH, SCENARIO_NAME))
    # roadmap_generator = RoadMapGenerator(SCENARIO_NAME)
    # roadmap_generator.generate(WALL_IMAGE, resolution, OUTPUT_PATH)
    # walkable_points = square_generator.build_point_dict(WALL_IMAGE, 0)
    # walkable_squares = square_generator.build_square_list(WALL_IMAGE, walkable_points)
    # data = {
    #     'width': int(WALL_IMAGE.shape[1]),
    #     'height': int(WALL_IMAGE.shape[1]),
    #     'squares': walkable_squares,
    #     'graph': square_generator.build_border_dict(walkable_squares),
    # }
    # graph_generator.build("%s/%s" % (OUTPUT_PATH, SCENARIO_NAME), data, resolution=resolution)

    # print("Completed! Use the following command to run the scenario in menge:")


parser = argparse.ArgumentParser(description="Generate files used to run simulations with Menge.")
parser.add_argument("path", help="path to the scenario XML file")
parser.add_argument("-b", "--behavior", help="path to the scenario behavior PNG file")
parser.add_argument("-w", "--wall", help="path to the scenario wall PNG file")
parser.add_argument("-o", "--output", help="directory to output to")
parser.add_argument("-r", "--resolution", default=0.5, type=float)
args = parser.parse_args()

XML_PATH = args.path
BEHAVIOR_PNG_PATH = XML_PATH.replace(".xml", ".png")
if args.behavior:
    BEHAVIOR_PNG_PATH = args.behavior
WALL_PNG_PATH = XML_PATH.replace(".xml", "Walls.png")
if args.wall:
    WALL_PNG_PATH = args.wall
SCENARIO_NAME = os.path.basename(XML_PATH)[:-4]
OUTPUT_PATH = SCENARIO_NAME
if args.output:
    OUTPUT_PATH = args.output

main(args.resolution)
