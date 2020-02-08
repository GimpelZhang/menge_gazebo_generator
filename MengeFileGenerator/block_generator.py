import numpy as np
import xml.etree.ElementTree as ET

from collections import defaultdict
from quadtree_map import QuadTreeMap


class BlockGenerator(object):
    def __init__(self):
        pass

    def generate(self, image, resolution):
        # wall_cells = self._get_wall_cells(image, resolution)
        quadmap = QuadTreeMap(image)
        boxs = quadmap.get_box()
        boxs = self._transform_coor(boxs, image)
        return self._generate_obstacle_set(boxs, image, resolution)

    def _get_wall_cells(self, image, resolution):
        cells = {}
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if np.sum(image[x][y][:]) == 0:
                    cell_x = resolution*y
                    cell_y = resolution*(image.shape[0] - 1 - x)
                    cells[(cell_x, cell_y)] = 1

        return cells

    def _transform_coor(self, boxs, image):
        new_boxs = []
        for box in boxs:
            x = box[1]
            y = image.shape[0] - box[0] - 1
            new_boxs.append([x, y, box[3], box[2]])
        return new_boxs

    def _generate_obstacle_set(self, boxs, image, resolution):
        root = ET.Element('ObstacleSet')
        root.set('type', 'explicit')
        root.set('class', '1')
        self._create_border(
            root, 
            image.shape[1]*resolution, 
            image.shape[0]*resolution
            )
        for box in boxs:
            self._create_obstacle(root, box, resolution)
        return root

    def _create_border(self, parent, width, height):
        node = ET.SubElement(parent, 'Obstacle')
        node.set('closed', '1')
        self._create_vertex(node, 0, height)
        self._create_vertex(node, width, height)
        self._create_vertex(node, width, 0)
        self._create_vertex(node, 0, 0)
        return node

    def _create_obstacle(self, parent, box, resolution):
        node = ET.SubElement(parent, 'Obstacle')
        node.set('closed', '1')
        x1 = box[0]
        x2 = box[0] + box[2]
        y1 = box[1] + 1
        y2 = box[1] - box[3] + 1
        self._create_vertex(node, x1*resolution, y2*resolution)
        self._create_vertex(node, x2*resolution, y2*resolution)
        self._create_vertex(node, x2*resolution, y1*resolution)
        self._create_vertex(node, x1*resolution, y1*resolution)
        return node

    def _create_vertex(self, parent, x, y):
        node = ET.SubElement(parent, 'Vertex')
        node.set('p_x', str(x))
        node.set('p_y', str(y))
        return node

if __name__ == "__main__":
    import imageio
    scene_name = "UTurn"
    wall_image = imageio.imread("../example/{}Walls.png".format(scene_name))
    generator = BlockGenerator()
    generator.generate(wall_image, 0.25)