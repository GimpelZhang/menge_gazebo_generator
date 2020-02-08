import numpy as np

class QuadTreeMap(object):
    def __init__(self, wall_image, pos=[0, 0]):
        self.children = None
        self.box = [pos[0], pos[1], wall_image.shape[0], wall_image.shape[1]]
        self.is_wall = False
        if np.sum(wall_image) != 0 and \
           wall_image.shape[0] > 1 and \
           wall_image.shape[1] > 1:
            self._split(wall_image)
        elif np.sum(wall_image) == 0:
            self.is_wall = True 

    def get_box(self):
        boxs = []
        if self.children:
            for child in self.children:
                boxs.extend(child.get_box())
            return boxs
        elif self.is_wall:
            return [self.box]
        else:
            return boxs

    def _split(self, image):
        self.children = [None for _ in range(4)]
        h_middle, w_middle = int(image.shape[1]*0.5), int(image.shape[0]*0.5)
        self.children[0] = QuadTreeMap(
            image[:w_middle, :h_middle, :], [self.box[0], self.box[1]]
            )
        self.children[1] = QuadTreeMap(
            image[w_middle:, :h_middle, :], [self.box[0] + w_middle, self.box[1]]
            )
        self.children[2] = QuadTreeMap(
            image[:w_middle, h_middle:, :], [self.box[0], self.box[1] + h_middle]
            )
        self.children[3] = QuadTreeMap(
            image[w_middle:, h_middle:, :], [self.box[0] + w_middle, self.box[1] + h_middle]
            )

if __name__ == "__main__":
    import imageio
    scene_name = "UTurn"
    wall_image = imageio.imread("../example/{}Walls.png".format(scene_name))
    quadmap = QuadTreeMap(wall_image)
    boxs = quadmap.get_box()
    new_image = 255 * np.ones_like(wall_image)
    for box in boxs:
        new_image[box[0]:box[0]+box[2], box[1]:box[1]+box[3], :] = 0

        new_image[box[0]:box[0]+box[2], box[1], :] = 125
        new_image[box[0]:box[0]+box[2], box[1]+box[3]-1, :] = 125
        new_image[box[0], box[1]:box[1]+box[3], :] = 125
        new_image[box[0]+box[2]-1, box[1]:box[1]+box[3], :] = 125

    imageio.imsave("{}.png".format(scene_name), new_image)
