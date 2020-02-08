import random
import scipy.misc

class Square:
    def __init__(self, y1, y2, x1, x2, can_cut, id_num):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.can_cut = can_cut
        self.id_num = id_num
        self.routers = []


    def __str__(self):
        return "id: %d x1: %d x2: %d y1: %d y2: %d can_cut: %s" % (
            self.id_num, self.x1, self.x2, self.y1, self.y2, self.can_cut)

    def __repr__(self):
        return "id: %d x1: %d x2: %d y1: %d y2: %d can_cut: %s" % (
            self.id_num, self.x1, self.x2, self.y1, self.y2, self.can_cut)

    def __eq__(self, other):
        if self.y1 == other.y1 and self.y2 == other.y2 and self.x1 == other.x1 and self.x2 == other.x2:
            return True
        else:
            return False


def side_ratio(sq1, sq2):
    if sq1.can_cut:
        ret = 1.1
        if sq1.y1 == sq2.y1 or sq1.y2 == sq2.y2:
            ret = (sq1.y2 - sq1.y1) / max((sq2.y2 - sq2.y1),1)
        elif sq1.x1 == sq2.x1 or sq1.x2 == sq2.x2:
            ret = (sq1.x2 - sq1.x1) / max((sq2.x2 - sq2.x1),1)
        if ret > 1:
            return 0
        else:
            return ret
    else:
        return 0


def area_ratio(sq1, sq2):
    if sq1.can_cut:
        if (sq1.y1 > sq2.y1 and sq1.y2 < sq2.y2):
            return (sq1.y2 - sq1.y1) / max((sq2.y2 - sq2.y1),1)
        elif (sq1.x1 > sq2.x1 and sq1.x2 < sq2.x2):
            return (sq1.x2 - sq1.x1) / max((sq2.x2 - sq2.x1),1)
        else:
            return 0
    else:
        return 0


def single_cut(sq1, sq2):
    new_squares = []

    if sq1.y1 == sq2.y1 and sq1.y2 == sq2.y2:
        if sq1.x1 < sq2.x1:
            new_squares.append(Square(sq1.y1, sq2.y2, sq1.x1, sq2.x2, True, sq1.id_num))
        else:
            new_squares.append(Square(sq1.y1, sq2.y2, sq2.x1, sq1.x2, True, sq1.id_num))

    elif sq1.x1 == sq2.x1 and sq1.x2 == sq2.x2:
        if sq1.y1 < sq2.y1:
            new_squares.append(Square(sq1.y1, sq2.y2, sq1.x1, sq1.x2, True, sq1.id_num))
        else:
            new_squares.append(Square(sq2.y1, sq1.y2, sq1.x1, sq1.x2, True, sq1.id_num))


    elif sq1.y1 == sq2.y1:  # cut on x2
        # print('x1', end=' ')
        if sq1.x1 < sq2.x1:
            new_squares.append(Square(sq1.y1, sq1.y2, sq1.x1, sq2.x2, True, sq1.id_num))
            new_squares.append(Square(sq1.y2 + 1, sq2.y2, sq2.x1, sq2.x2, False, sq2.id_num))
            # print('we')
        else:
            new_squares.append(Square(sq1.y1, sq1.y2, sq2.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq1.y2 + 1, sq2.y2, sq2.x1, sq2.x2, False, sq2.id_num))
            # print('ew')

    elif sq1.y2 == sq2.y2:
        # print('x2', end=' ')
        if sq1.x1 < sq2.x1:
            new_squares.append(Square(sq1.y1, sq1.y2, sq1.x1, sq2.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq1.y1 - 1, sq2.x1, sq2.x2, False, sq2.id_num))
            # print('we')
        else:
            new_squares.append(Square(sq1.y1, sq1.y2, sq2.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq1.y1 - 1, sq2.x1, sq2.x2, False, sq2.id_num))
            # print('ew')

    elif sq1.x1 == sq2.x1:
        # print('y1', end=' ')
        if sq1.y1 < sq2.y1:
            new_squares.append(Square(sq1.y1, sq2.y2, sq1.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq1.x2 + 1, sq2.x2, False, sq2.id_num))
            # print('ns')
        else:
            new_squares.append(Square(sq2.y1, sq1.y2, sq1.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq1.x2 + 1, sq2.x2, False, sq2.id_num))
            # print('sn')

    elif sq1.x2 == sq2.x2:
        # print('y2', end=' ')
        if sq1.y1 < sq2.y1:
            new_squares.append(Square(sq1.y1, sq2.y2, sq1.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq2.x1, sq1.x1 - 1, False, sq2.id_num))
            # print('ns')
        else:
            new_squares.append(Square(sq2.y1, sq1.y2, sq1.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq2.x1, sq1.x1 - 1, False, sq2.id_num))
            # print('sn')

    #print("CUT")
    return new_squares


def double_cut(sq1, sq2):
    new_squares = []
    if sq1.y1 > sq2.y1 and sq1.y2 < sq2.y2:
        if sq1.x2 + 1 == sq2.x1:
            new_squares.append(Square(sq1.y1, sq1.y2, sq1.x1, sq2.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq1.y1 - 1, sq2.x1, sq2.x2, False, sq2.id_num))
            new_squares.append(Square(sq1.y2 + 1, sq2.y2, sq2.x1, sq2.x2, False, -1))
        else:
            new_squares.append(Square(sq1.y1, sq1.y2, sq2.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq1.y1 - 1, sq2.x1, sq2.x2, False, sq2.id_num))
            new_squares.append(Square(sq1.y2 + 1, sq2.y2, sq2.x1, sq2.x2, False, -1))


    elif sq1.x1 > sq2.x1 and sq1.x2 < sq2.x2:
        if sq1.y2 + 1 == sq2.y1:
            new_squares.append(Square(sq1.y1, sq2.y2, sq1.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq2.x1, sq1.x1 - 1, False, sq2.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq1.x2 + 1, sq2.x2, False, -1))
        else:
            new_squares.append(Square(sq2.y1, sq1.y2, sq1.x1, sq1.x2, True, sq1.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq2.x1, sq1.x1 - 1, False, sq2.id_num))
            new_squares.append(Square(sq2.y1, sq2.y2, sq1.x2 + 1, sq2.x2, False, -1))

    return new_squares


MIDPOINT_DIVISOR = 20
def rebuild(square_list, border_dict):

    for i in range(len(square_list)):
        border_dict[i] = []
        square_list[i].routers = []

    for i in range(len(square_list)):
        square = square_list[i]

        for next_index in range(i + 1, len(square_list)):
            next_square = square_list[next_index]

            if next_square.x1 >= square.x1 and next_square.x2 <= square.x2:
                if next_square.y1 == square.y2 + 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (int((next_square.x2 - next_square.x1) * (m / MIDPOINT_DIVISOR)) + next_square.x1, next_square.y1)
                        )
                        square_list[i].routers.append(
                            (int((next_square.x2 - next_square.x1) * (m / MIDPOINT_DIVISOR)) + next_square.x1, square.y2)
                        )

                elif next_square.y2 == square.y1 - 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (int((next_square.x2 - next_square.x1) * (m / MIDPOINT_DIVISOR)) + next_square.x1, next_square.y2)
                        )
                        square_list[i].routers.append(
                            (int((next_square.x2 - next_square.x1) * (m / MIDPOINT_DIVISOR)) + next_square.x1, square.y1)
                        )

            elif next_square.y1 >= square.y1 and next_square.y2 <= square.y2:
                if next_square.x1 == square.x2 + 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (next_square.x1, int((next_square.y2 - next_square.y1) * (m / MIDPOINT_DIVISOR)) + next_square.y1)
                        )
                        square_list[i].routers.append(
                            (square.x2, int((next_square.y2 - next_square.y1) * (m / MIDPOINT_DIVISOR)) + next_square.y1)
                        )

                elif next_square.x2 == square.x1 - 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (next_square.x2, int((next_square.y2 - next_square.y1) * (m / MIDPOINT_DIVISOR)) + next_square.y1)
                        )
                        square_list[i].routers.append(
                            (square.x1, int((next_square.y2 - next_square.y1) * (m / MIDPOINT_DIVISOR)) + next_square.y1)
                        )

            elif square.x1 >= next_square.x1 and square.x2 <= next_square.x2:
                if square.y1 == next_square.y2 + 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (int((square.x2 - square.x1) * (m / MIDPOINT_DIVISOR)) + square.x1, square.y1)
                        )
                        square_list[i].routers.append(
                            (int((square.x2 - square.x1) * (m / MIDPOINT_DIVISOR)) + square.x1, next_square.y2)
                        )

                elif square.y2 == next_square.y1 - 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (int((square.x2 - square.x1) * (m / MIDPOINT_DIVISOR)) + square.x1,square.y2)
                        )
                        square_list[i].routers.append(
                            (int((square.x2 - square.x1) * (m / MIDPOINT_DIVISOR)) + square.x1, next_square.y1)
                        )

            elif square.y1 >= next_square.y1 and square.y2 <= next_square.y2:
                if square.x1 == next_square.x2 + 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (square.x1, int((square.y2 - square.y1) * (m / MIDPOINT_DIVISOR)) + square.y1)
                        )
                        square_list[i].routers.append(
                            (next_square.x2, int((square.y2 - square.y1) * (m / MIDPOINT_DIVISOR)) + square.y1)
                        )

                elif square.x2 == next_square.x1 - 1:
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[next_index].routers.append(
                            (next_square.x1, int((square.y2 - square.y1) * (m / MIDPOINT_DIVISOR)) + square.y1)
                        )
                        square_list[i].routers.append(
                            (square.x2, int((square.y2 - square.y1) * (m / MIDPOINT_DIVISOR)) + square.y1)
                        )


            elif next_square.y2 == square.y1 - 1:

                # Hanging Case 1
                # next_square is on the top of square
                # right side of next_square extends pass right side of square
                if (square.x1 <= next_square.x1) and (square.x2 < next_square.x2) and (square.x2 > next_square.x1):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            ((next_square.x1 + square.x2) * (m / MIDPOINT_DIVISOR), square.y1)
                        )
                        square_list[next_index].routers.append(
                            ((next_square.x1 + square.x2) * (m / MIDPOINT_DIVISOR), next_square.y2)
                        )

                # Hanging Case 2
                # next_square is on the top of square
                # left side of next square extends pass the left side of square
                elif (square.x1 >= next_square.x1) and (square.x2 > next_square.x2) and (square.x1 < next_square.x2):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            ((square.x1 + next_square.x2) * (m / MIDPOINT_DIVISOR), square.y1)
                        )
                        square_list[next_index].routers.append(
                            ((square.x1 + next_square.x2) * (m / MIDPOINT_DIVISOR), next_square.y2)
                        )

            elif square.y2 == next_square.y1 - 1:

                # Hanging Case 3
                # square is on top of next_square
                # right side of square extends pass right side of next_square
                if (next_square.x1 <= square.x1) and (next_square.x2 < square.x2) and (next_square.x2 > square.x1):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            ((square.x1 + next_square.x2) * (m / MIDPOINT_DIVISOR), square.y2)
                        )
                        square_list[next_index].routers.append(
                            ((square.x1 + next_square.x2) * (m / MIDPOINT_DIVISOR), next_square.y1)
                        )

                # Hanging Case 4
                # square is on top of next_square
                # left side of square extends pass the left side of next_square
                elif (next_square.x1 >= square.x1) and (next_square.x2 > square.x2) and (next_square.x1 < square.x2):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            ((next_square.x1 + square.x2) * (m / MIDPOINT_DIVISOR), square.y2)
                        )
                        square_list[next_index].routers.append(
                            ((next_square.x1 + square.x2) * (m / MIDPOINT_DIVISOR), next_square.y1)
                        )

            elif next_square.x2 == square.x1 - 1:

                # Hanging Case 5
                # next_square is to the left of square
                # bottom side of square extends pass the bottom side of next square
                if (square.y1 >= next_square.y1) and (square.y2 > next_square.y2) and (square.y1 < next_square.y2):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            (square.x1, (square.y1 + next_square.y2) * (m / MIDPOINT_DIVISOR))
                        )
                        square_list[next_index].routers.append((
                            next_square.x2, (square.y1 + next_square.y2) * (m / MIDPOINT_DIVISOR))
                        )

                # Hanging Case 6
                # next_square is to the left of square
                # top side of square extends pass the top side of next_square
                elif (square.y1 <= next_square.y1) and (square.y2 < next_square.y2) and (square.y2 > next_square.y1):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            (square.x1, (next_square.y1 + square.y2) * (m / MIDPOINT_DIVISOR))
                        )
                        square_list[next_index].routers.append(
                            (next_square.x2, (next_square.y1 + square.y2) * (m / MIDPOINT_DIVISOR))
                        )

            elif square.x2 == next_square.x1 - 1:

                # Hanging Case 7
                # square is to the left of next_square
                # bottom side of square extends pass bottom side of next_square
                if (square.y1 >= next_square.y1) and (square.y2 > next_square.y2) and (square.y1 < next_square.y2):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            (square.x1, (square.y1 + next_square.y2) * (m / MIDPOINT_DIVISOR))
                        )
                        square_list[next_index].routers.append((
                            next_square.x2, (square.y1 + next_square.y2) * (m / MIDPOINT_DIVISOR))
                        )

                # Hanging Case 8
                # square is to the left of next_square
                # top side of square extends pass top side of next_square
                elif (square.y1 <= next_square.y1) and (square.y2 < next_square.y2) and (square.y2  > next_square.y1):
                    border_dict[i].append(next_index)
                    border_dict[next_index].append(i)
                    for m in range(MIDPOINT_DIVISOR + 1):
                        square_list[i].routers.append(
                            (square.x2, (next_square.y1 + square.y2) * (m / MIDPOINT_DIVISOR))
                        )
                        square_list[next_index].routers.append(
                            (next_square.x1, (next_square.y1 + square.y2) * (m / MIDPOINT_DIVISOR))
                        )


# build_squares(list(tuple[4])
# old_squares are tuple[4] coordinates of top left and bottom right squares
# Returns: a list of square objects
def build_squares(old_squares):
    square_list = []
    for i, s in enumerate(old_squares):
        square_list.append(Square(s[0], s[1], s[2], s[3], True, i))
    return square_list


# merge_squares(list(square), border_dict)
# Reduces the amount of squares by merging overlapping regions
def merge_squares(square_list, border_dict):
    while True:
        i = 0
        rebuilt = False

        while i < len(square_list) and not rebuilt:

            for n in border_dict[i]:

                s_rat = side_ratio(square_list[i], square_list[n])

                if s_rat > 0.6:
                    new_squares = single_cut(square_list[i], square_list[n])
                    s1 = square_list[n]
                    s2 = square_list[i]
                    square_list.remove(s1)
                    square_list.remove(s2)
                    square_list.extend(new_squares)
                    rebuild(square_list, border_dict)
                    rebuilt = True
                    break

                a_rat = area_ratio(square_list[i], square_list[n])

                if a_rat > 0.6:
                    new_squares = double_cut(square_list[i], square_list[n])
                    s1 = square_list[n]
                    s2 = square_list[i]
                    square_list.remove(s1)
                    square_list.remove(s2)
                    square_list.append(new_squares[0])
                    square_list.append(new_squares[1])
                    new_squares[2].id_num = len(square_list)
                    square_list.append(new_squares[2])
                    rebuild(square_list, border_dict)
                    rebuilt = True
                    break

            i += 1

        if not rebuilt:
            rebuild(square_list, border_dict)
            break


# Checks if the two coordinate pairs are nearby
def is_adjacent(c1, c2):
    if c1[0] + 1 == c2[0] or c1[0] - 1 == c2[0]:
        return c1[1] == c2[1]
    elif c1[1] + 1 == c2[1] or c1[1] - 1 == c2[1]:
        return c1[0] == c2[0]
    else:
        return False


def add_if_absent(edge, edges):
    vid, other_vid = edge

    if vid != other_vid and edges.get((vid, other_vid)) is None and edges.get((other_vid, vid)) is None:
        edges[edge] = True


def graph_squares(squares, vmap, edges, sim_height):
    for square_index, s in enumerate(squares):
        x1, x2 = s.x1, s.x2
        y1, y2 = max(0, sim_height - s.y1 - 1), max(0, sim_height - s.y2 - 1)
        corners = [
            (x1, y2),  # Top Left Vertex
            (x1, y1),  # Bottom Left Vertex
            (x2, y1),  # Top Right Vertex
            (x2, y2),  # Bottom Right Vertex
        ]

        # Add new vertices to the vertex map
        for corner in corners:
            if vmap.get(corner) is None:
                vmap[corner] = len(vmap.keys())

        # Add routers to the vertex map
        for i, vertex in enumerate(s.routers):
            vertex = vertex[0], max(0, sim_height - vertex[1] - 1)
            s.routers[i] = vertex
            if vmap.get(vertex) is None:
                vmap[vertex] = len(vmap.keys())

        # Add edges to the newly added corner vertices
        for i in range(len(corners)):
            vid = vmap[corners[i]]
            for next in range(i + 1, len(corners)):
                next_vid = vmap[corners[next]]
                add_if_absent((vid, next_vid), edges)

        # Add edges from the router to the corners
        for vertex in s.routers:
            vid = vmap[vertex]
            for corner in corners:
                corner_vid = vmap[corner]
                add_if_absent((vid, corner_vid), edges)

        # Add edges connecting internal routers
        if len(s.routers) > 1:
            for i in range(len(s.routers)):
                vid = vmap[s.routers[i]]
                for next in range(i + 1, len(s.routers)):
                    other_vid = vmap[s.routers[next]]
                    add_if_absent((vid, other_vid), edges)


def connect_graph_squares(squares, vmap, edges, border_dict):

    for sid in border_dict.keys():
        square = squares[sid]
        for adjacent_sid in border_dict[sid]:
            adjacent_square = squares[adjacent_sid]
            for router in square.routers:
                vid = vmap[router]
                for adjacent_router in adjacent_square.routers:
                    other_vid = vmap[adjacent_router]
                    if is_adjacent(router, adjacent_router):
                        add_if_absent((vid, other_vid), edges)


# write_to_TXT(list(vertices), list(edges), string)
# Writes the given vertices and edges to file
def write_to_TXT(vmap, edges, fileName, resolution=0.5):

    outfile = open(fileName + '.txt', 'w')

    outfile.write('%d\n' % len(vmap.keys()))
    inverse_vmap = {y: x for x, y in vmap.items()}
    for i in range(len(vmap.keys())):
        vid = i
        degree = 0
        for v1, v2 in edges.keys():
            if vid == v1 or vid == v2:
                degree += 1

        outfile.write("%d %f %f\n" % (degree, inverse_vmap[i][0]*resolution, inverse_vmap[i][1]*resolution))

    outfile.write('%d\n' % len(edges))
    for edge in edges.keys():
        outfile.write('%d %d\n' % (edge[0], edge[1]))

    outfile.close()


def build(base_name, data, resolution=0.5):

    # Stores the vertex ID of a certain x, y coordinate.
    # (x, y): vertexID
    vmap = {}
    edges = {}
    square_list = build_squares(data['squares'])
    merge_squares(square_list, data['graph'])

    graph_squares(square_list, vmap, edges, data['height'])
    connect_graph_squares(square_list, vmap, edges, data['graph'])


    '''
    WALL_IMAGE = scipy.misc.imread('%s.png' % 'marathon_street_map_full', mode='RGBA')
    color_list = [(random.randrange(255), random.randrange(255), random.randrange(255), 128) for i in range(2000)]
    for xx, sq in enumerate(square_list):
        for i in range(sq.y1, sq.y2 + 1):
            for j in range(sq.x1, sq.x2 + 1):
                WALL_IMAGE[i][j] = (color_list[xx])
    scipy.misc.imsave('marathon_street_squares.png', WALL_IMAGE)
    '''


    write_to_TXT(vmap, edges, base_name, resolution=resolution)
