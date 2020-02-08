import numpy as np

from collections import defaultdict

class RoadMapGenerator(object):
    def __init__(self, scene_name):
        self.scene_name = scene_name

    def generate(self, image, resolution, output_path):
        free_cells = self._get_free_cells(image, resolution)
        self._check_collision(free_cells, output_path, resolution)

    def _get_free_cells(self, image, resolution):
        cells = defaultdict(int)
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if np.sum(image[x][y][:]) == 255*3:
                    # cell_x = np.round(resolution*y)
                    # cell_y = np.round(
                    #     resolution*(image.shape[0] - 1 - x)
                    #     )
                    # cells[(cell_x, cell_y)] += 1

                    cell_x = y
                    cell_y = image.shape[0] - x - 1
                    cells[(cell_x, cell_y)] = 1

        # free_cells = cells
        free_cells = {}
        for pos in cells.keys():
            free_number = 0
            for next_cell in [[0, -1], 
                              [0, 1], 
                              [-1, 0], 
                              [1, 0], 
                              [-1, -1], 
                              [-1, 1], 
                              [1, -1], 
                              [1, 1]]:
                new_x = pos[0] + next_cell[0]
                new_y = pos[1] + next_cell[1]
                new_pos = (new_x, new_y)
                if new_pos in cells:
                    free_number += 1

            if free_number == 8:
                free_cells[pos] = 1

        # free_cells = {}
        # free_threshold = np.max(cells.values())
        # for pos, v in cells.items():
        #     if v >= (0.125/resolution)*free_threshold:
        #         free_cells[pos] = 1

        return free_cells

    def _check_collision(self, free_cells, output_path, resolution):
        outfile = open("{}/{}.txt".format(
            output_path, self.scene_name), 'w'
            )        
        checked_cells = defaultdict(list)
        edge_dict = defaultdict(dict)
        edges = []
        outfile.write("%d\n" % len(free_cells.keys()))
        for i, pos in enumerate(free_cells.keys()):
            for next_cell in [[0, -1], 
                              [0, 1], 
                              [-1, 0], 
                              [1, 0], 
                              [-1, -1], 
                              [-1, 1], 
                              [1, -1], 
                              [1, 1]]:
                new_x = pos[0] + next_cell[0]
                new_y = pos[1] + next_cell[1]
                new_pos = (new_x, new_y)
                if new_pos in free_cells:
                    checked_cells[pos].append(new_pos)
                    if not ((new_pos in checked_cells[pos]) and \
                            (pos in checked_cells[new_pos])):
                        edge_dict[new_pos][pos] = i
                    else:
                        j = edge_dict[pos][new_pos]
                        edges.append([j, i])
            
            num_edges = len(checked_cells[pos])
            outfile.write("%d %f %f\n" % (num_edges, 
                                          resolution*pos[0], 
                                          resolution*pos[1]))

        outfile.write('%d\n' % len(edges))
        for edge in edges:
            outfile.write("%d %d\n" % (edge[0], edge[1]))

        outfile.close()

if __name__ == "__main__":
    import imageio
    scene_name = "UTurn"
    wall_image = imageio.imread("../example/{}Walls.png".format(scene_name))
    generator = RoadMapGenerator(scene_name)
    generator.generate(wall_image, 0.25, "../output/{}".format(scene_name))
                    

         

