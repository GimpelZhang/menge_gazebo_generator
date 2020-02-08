#!/usr/bin/env python

import os
import argparse
import imageio
import scipy.misc
import xml.dom.minidom as xdm
import xml.etree.ElementTree as et
import graph_generator
import square_generator
import wall_generator
import xml_generator

from roadmap_generator import RoadMapGenerator
from block_generator import BlockGenerator


BEHAVIOR_IMAGE = None
WALL_IMAGE = None

MAIN_XML = None
SCENE_XML = et.parse('base_scene.xml').getroot()
BEHAVIOR_XML = et.Element('BFSM')
VIEWER_XML = et.parse('base_viewer.xml').getroot()
COLOR_DICTIONARY = {}

def create_color_dictionary(image, resolution=0.5):
    height = image.shape[0]
    width = image.shape[1]
    color_coords = {}
    for x in range(width):
        for y in range(height):
            rgb = tuple(image[y][x][:3])
            if color_coords.get(rgb) is None:
                color_coords[rgb] = []
            color_coords[rgb].append((x*resolution, (height - y)*resolution))
    return color_coords


def get_node_rgb(node):
    r = int(node.attrib['r'])
    g = int(node.attrib['g'])
    b = int(node.attrib['b'])
    return tuple((r, g, b))


def add_agents(group_id, group_node):

    speed = 1
    try:
        speed = int(group_node.attrib['speed'])
    except KeyError:
        print("[WARNING] Missing 'speed' attribute in group %d. Using default value %d." % (group_id, speed))
    except ValueError:
        print("[WARNING] Invalid type for 'speed' attribute in group %d. Using default value %d." % (group_id, speed))
    finally:
        node = xml_generator.make_agent_profile(group_id, speed)
        SCENE_XML.append(node)

    amount = 1
    try:
        amount = int(group_node.attrib['amount'])
    except KeyError:
        print("[WARNING] Missing 'amount' attribute in group %d. Using default value %d." % (group_id, amount))
    except ValueError:
        print("[WARNING] Invalid type for 'amount' attribute in group %d. Using default value %d." % (group_id, amount))
    finally:
        node = xml_generator.make_agent_group(group_id, amount)
        SCENE_XML.append(node)


def add_goal_sets(group_id, group_node, total_goalsets):

    for goal_set_id, goal_set_node in enumerate(group_node.findall('GoalSet')):

        capacity = 1
        try:
            capacity = int(goal_set_node.attrib['capacity'])
        except KeyError:
            print("[WARNING] Missing 'capacity' attribute in group %d goal set %d. Using default value %d." %
                  (group_id, goal_set_id, capacity))
        except ValueError:
            print("[WARNING] Invalid type for 'capacity' attribute in group %d goal set %d. Using default value %d." %
                  (group_id, goal_set_id, capacity))

        rgb = None
        try:
            rgb = get_node_rgb(goal_set_node.find('Color'))
        except KeyError:
            print("[ERROR] Missing 'r', 'g', 'b' attributes in group %d goal set %d color." %
                  (group_id, goal_set_id))
            return False
        except ValueError:
            print("[ERROR] Invalid type for 'r', 'g', 'b' attributes in group %d goal set %d." %
                  (group_id, goal_set_id))
            return False

        destinations = None
        try:
            destinations = COLOR_DICTIONARY[rgb]
        except KeyError:
            print("[ERROR] Could not find pixels with an RGB value of %s in %s.png when trying to create group %d goal set %d." %
                  (rgb, SCENARIO_NAME, group_id, goal_set_id))
            return False

        node = xml_generator.make_goal_set(goal_set_id + total_goalsets, capacity, destinations)
        BEHAVIOR_XML.append(node)

    return True


def add_spawn(group_id, group_node):

    min = 0
    try:
        min = int(group_node.find('Spawn').attrib['min'])
    except KeyError:
        print("[WARNING] Missing 'min' attribute in group %d spawn. Using default value %d." %
              (group_id, min))
    except ValueError:
        print("[WARNING] Invalid type for 'min' attribute in group %d spawn. Using default value %d." %
              (group_id, min))

    max = 0
    try:
        max = int(group_node.find('Spawn').attrib['max'])
    except KeyError:
        print("[WARNING] Missing 'max' attribute in group %d spawn. Using default value %d" %
              (group_id, max))
    except ValueError:
        print("[WARNING] Invalid type for 'max' attribute in group %d spawn. Using default value %d." %
              (group_id, max))

    rgb = None
    try:
        rgb = get_node_rgb(group_node.find('Spawn').find('Color'))
    except KeyError:
        print("[ERROR] Missing 'r', 'g', 'b' attributes in group %d spawn." % group_id)
        return False
    except ValueError:
        print("[ERROR] Invalid type for 'r', 'g', 'b' attributes in group %d spawn." % group_id)
        return False

    state_start_name = 'Start_%d' % group_id
    start_node = xml_generator.make_state_static(state_start_name, '0', 'zero')
    BEHAVIOR_XML.append(start_node)

    state_wait_name = 'Start_Wait_%d' % group_id
    wait_node = xml_generator.make_state_static(state_wait_name, '0', 'zero')
    BEHAVIOR_XML.append(wait_node)

    # start_wait_tran = xml_generator.make_transition_timer(state_start_name, state_wait_name, min, max)
    start_wait_tran = xml_generator.make_transition_auto(state_start_name, state_wait_name)
    BEHAVIOR_XML.append(start_wait_tran)

    locations = []
    try:
        for spawn_id, location in enumerate(COLOR_DICTIONARY[rgb]):
            name = 'Spawn_%d_%d' % (group_id, spawn_id)
            locations.append(tuple((name, '1')))
            spawn_node = xml_generator.make_state_teleport(name, location)
            BEHAVIOR_XML.append(spawn_node)
    except KeyError:
        print(
            "[ERROR] Could not find pixels with an RGB value of %s in %s.png when trying to create group %d spawn." %
            (rgb, SCENARIO_NAME, group_id))
        return False

    spawn_tran = xml_generator.make_transition_random(state_wait_name, locations)
    BEHAVIOR_XML.append(spawn_tran)

    destinations = []
    for destination_id, destination_node in enumerate(group_node.find('Spawn').findall('Transition')):

        to = 0
        try:
            to = int(destination_node.attrib['to'])
        except KeyError:
            print("[WARNING] Missing 'to' attribute in spawn for group %d transition %d. Using default value %d." %
                  (group_id, destination_id, to))
        except ValueError:
            print("[WARNING] Invalid type for 'to' attribute in spawn for group %d transition %d. Using default value %d." %
                (group_id, destination_id, to))

        chance = 1
        try:
            chance = float(destination_node.attrib['chance'])
            destinations.append(tuple(('Travel_%d_%d' % (group_id, to), chance)))
        except KeyError:
            print("[WARNING] Missing 'chance' attribute in spawn for group %d transition %d. Using default value %d." %
                  (group_id, destination_id, chance))
        except ValueError:
            print("[WARNING] Invalid type for 'chance' attribute in spawn for group %d transition %d. Using default value %d." %
                (group_id, destination_id, chance))

    spawn_names = [x[0] for x in locations]
    tran = xml_generator.make_transition_random(','.join(spawn_names), destinations)
    BEHAVIOR_XML.append(tran)
    return True


def add_goals(group_id, group_node, total_goalsets):

    for goal_set_id, goal_set_node in enumerate(group_node.findall('GoalSet')):
        
        state_travel_name = 'Travel_%d_%d' % (group_id, goal_set_id)
        travel_node = xml_generator.make_state_travel(state_travel_name, goal_set_id + total_goalsets, SCENARIO_NAME)
        BEHAVIOR_XML.append(travel_node)

        state_arrive_name = 'Arrive_%d_%d' % (group_id, goal_set_id)
        arrive_node = xml_generator.make_state_static(state_arrive_name, '1', 'goal')
        BEHAVIOR_XML.append(arrive_node)

        travel_arrive_tran = xml_generator.make_transition_goal_reached(state_travel_name, state_arrive_name)
        BEHAVIOR_XML.append(travel_arrive_tran)

        # Wait at goal state
        state_wait_name = 'Wait_%d_%d' % (group_id, goal_set_id)
        wait_node = xml_generator.make_state_static(state_wait_name, '0', 'goal')
        BEHAVIOR_XML.append(wait_node)

        min = 0
        try:
            min = int(goal_set_node.attrib['min'])
        except KeyError:
            print("[WARNING] Missing 'min' attribute in group %d goal set %d. Using default value %d." %
                  (group_id, goal_set_id, min))
        except ValueError:
            print("[WARNING] Invalid type for 'min' attribute in group %d goal set %d. Using default value %d." %
                  (group_id, goal_set_id, min))

        max = 0
        try:
            max = int(goal_set_node.attrib['max'])
        except KeyError:
            print("[WARNING] Missing 'max' attribute in group %d goal set %d. Using default value %d." %
                  (group_id, goal_set_id, max))
        except ValueError:
            print("[WARNING] Invalid type for 'max' attribute in group %d goal set %d. Using default value %d." %
                  (group_id, goal_set_id, max))
        # timer_tran = xml_generator.make_transition_timer(state_arrive_name, state_wait_name, min, max)
        if len(group_node.findall('GoalSet')) == (goal_set_id+1):
            start_name = "Start_Wait_%d" % (group_id)
        else:
            start_name = "Travel_{}_{}".format(group_id, goal_set_id+1)

        # timer_tran = xml_generator.make_transition_auto(state_arrive_name, start_name)
        # BEHAVIOR_XML.append(timer_tran)

        next_destinations = []
        for transition_id, transition_node in enumerate(goal_set_node.findall('Transition')):
            to = goal_set_id
            try:
                to = int(transition_node.attrib['to'])
            except KeyError:
                print("[WARNING] Missing 'to' attribute in group %d goal set %d transition %d. Using default value %d." %
                      (group_id, goal_set_id, transition_id, to))
            except ValueError:
                print("[WARNING] Invalid type for 'to' attribute in group %d goal set %d transition %d. Using default value %d." %
                      (group_id, goal_set_id, transition_id, to))

            chance = 1
            try:
                chance = float(transition_node.attrib['chance'])
            except KeyError:
                print("[WARNING] Missing 'chance' attribute in group %d goal set %d transition %d. Using default value %d." %
                    (group_id, goal_set_id, transition_id, chance))
            except ValueError:
                print("[WARNING] Invalid type for 'chance' attribute in group %d goal set %d transition %d. Using default value %d." %
                    (group_id, goal_set_id, transition_id, chance))

            if goal_set_id == int(to):
                next_destinations.append(tuple(("Start_Wait_%d" % (group_id), chance)))
            else:
                next_destinations.append(tuple(('Travel_%d_%d' % (group_id, to), chance)))
        destination_tran = xml_generator.make_transition_random(state_arrive_name, next_destinations)
        # destination_tran = xml_generator.make_transition_auto(state_wait_name, next_destinations[0])
        # print destination_tran
        BEHAVIOR_XML.append(destination_tran)


def create_XML_link():
    root = et.Element('Project')
    root.set('scene', '%sS.xml' % SCENARIO_NAME)
    root.set('behavior', '%sB.xml' % SCENARIO_NAME)
    root.set('view', '%sV.xml' % SCENARIO_NAME)
    root.set('model', 'orca')
    root.set('dumpPath', 'images/%s' % SCENARIO_NAME)
    root.set('duration', str(1000000000))
    return root


def create_XML_scene_behavior():

    total_goalsets = 0
    for group_id, group_node in enumerate(MAIN_XML.findall('Group')):

        if not add_goal_sets(group_id, group_node, total_goalsets):
            return False

        if not add_spawn(group_id, group_node):
            return False

        add_agents(group_id, group_node)
        add_goals(group_id, group_node, total_goalsets)
        total_goalsets += len(group_node.findall('GoalSet'))

    return True


def create_XML_viewer():

    x = BEHAVIOR_IMAGE.shape[1] / 2 - 50
    y = BEHAVIOR_IMAGE.shape[0] / 2 - 50
    xtgt = x
    ytgt = y + .01
    scale = .5

    camera = VIEWER_XML.find('Camera')
    camera.set('xpos', str(x))
    camera.set('ypos', str(y))
    camera.set('xtgt', str(xtgt))
    camera.set('ytgt', str(ytgt))
    camera.set('orthoScale', str(scale))


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

    global MAIN_XML, BEHAVIOR_IMAGE, WALL_IMAGE, COLOR_DICTIONARY
    MAIN_XML = et.parse(XML_PATH).getroot()
    BEHAVIOR_IMAGE = imageio.imread(BEHAVIOR_PNG_PATH)
    WALL_IMAGE = imageio.imread(WALL_PNG_PATH)

    if not os.path.exists("%s/" % OUTPUT_PATH):
        print("Creating output directory './%s/'" % OUTPUT_PATH)
        os.makedirs("%s/" % OUTPUT_PATH)

    print("Creating link file '%s/%s.xml'..." % (OUTPUT_PATH, SCENARIO_NAME))
    link_xml = create_XML_link()
    write_to_XML(link_xml, '%s/%s' % (OUTPUT_PATH, SCENARIO_NAME))

    print("Creating viewer file '%s/%sV.xml'..." % (OUTPUT_PATH, SCENARIO_NAME))
    create_XML_viewer()
    write_to_XML(VIEWER_XML, '%s/%sV' % (OUTPUT_PATH, SCENARIO_NAME))

    print("Creating behavior file '%s/%sB.xml..." % (SCENARIO_NAME, SCENARIO_NAME))
    COLOR_DICTIONARY = create_color_dictionary(BEHAVIOR_IMAGE, resolution=resolution)
    if not create_XML_scene_behavior():
        return
    write_to_XML(BEHAVIOR_XML, '%s/%sB' % (OUTPUT_PATH, SCENARIO_NAME))

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

    print("Creating road map file %s/%s.txt..." % (OUTPUT_PATH, SCENARIO_NAME))
    roadmap_generator = RoadMapGenerator(SCENARIO_NAME)
    roadmap_generator.generate(WALL_IMAGE, resolution, OUTPUT_PATH)
    # walkable_points = square_generator.build_point_dict(WALL_IMAGE, 0)
    # walkable_squares = square_generator.build_square_list(WALL_IMAGE, walkable_points)
    # data = {
    #     'width': int(WALL_IMAGE.shape[1]),
    #     'height': int(WALL_IMAGE.shape[1]),
    #     'squares': walkable_squares,
    #     'graph': square_generator.build_border_dict(walkable_squares),
    # }
    # graph_generator.build("%s/%s" % (OUTPUT_PATH, SCENARIO_NAME), data, resolution=resolution)

    print("Completed! Use the following command to run the scenario in menge:")


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
