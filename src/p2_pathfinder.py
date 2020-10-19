from heapq import heappop, heappush
from math import sqrt
def find_path (source_point, destination_point, mesh):
    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    print("===========================================================================")
    print(f'Going from {source_point} to {destination_point}')
    key_boxes = find_boxes(source_point, destination_point, mesh)
    print(f'key boxes is {key_boxes}')
    start_box = key_boxes['start']
    end_box = key_boxes['end']

    fwd_a_star = AStarIterator(mesh, source_point, destination_point, start_box, end_box)
    fwd_path = []
    fwd_boxes = {}

    bwd_a_star = AStarIterator(mesh, destination_point, source_point, end_box, start_box)
    while (bwd_a_star.current_point not in fwd_a_star.pt_came_from \
            or fwd_a_star.current_point not in bwd_a_star.pt_came_from):
        bwd_a_star.iterate()
        fwd_a_star.iterate()

    common_point = bwd_a_star.current_point
    bptr = bwd_a_star.pt_came_from[common_point]
    fptr = fwd_a_star.pt_came_from[common_point]
    fwd_boxes[bwd_a_star.points[common_point][1]] = 1
    fwd_boxes[fwd_a_star.points[common_point][1]] = 1

    while fptr is not source_point:
        fwd_path.append(fptr)
        fwd_boxes[fwd_a_star.points[fptr][1]] = 1
        fptr = fwd_a_star.pt_came_from[fptr]

    while bptr is not destination_point:
        fwd_path.insert(0, bptr)
        fwd_boxes[bwd_a_star.points[bptr][1]] = 1
        bptr = bwd_a_star.pt_came_from[bptr]

    fwd_path.append(source_point)
    fwd_path.insert(0, destination_point)
    print("Finished computation")

    return fwd_path, fwd_boxes.keys()


def find_boxes(start, end, mesh):
    boxes = {}
    for box in mesh['boxes']:
        if box[1] >= start[0] >= box[0]:
            if box[3] >= start[1] >= box[2]:
                print(f'found start box, {start} in {box}')
                boxes['start'] = box
        if box[1] >= end[0] >= box[0]:
            if box[3] >= end[1] >= box[2]:
                print(f'found end box, {end} in {box}')
                boxes['end'] = box
    return boxes


def find_least_dist_to_box(b1, b2, point):
    x_range = [max(b1[0], b2[0]), min(b1[1], b2[1])]
    y_range = [max(b1[2], b2[2]), min(b1[3], b2[3])]

    # print("    find_dist: ", b1, b2, point)
    # print("    x_range:", x_range, "y_range:", y_range)
    # if b1[3] == b2[2]:
    #     print("    Right neighbor")
    # elif b1[2] == b2[3]:
    #     print("    Left neighbor")
    # elif b1[1] == b2[0]:
    #     print("    Bottom neighbor")
    # elif b1[0] == b2[1]:
    #     print("    Top neighbor")

    new_x1 = x_range[0]
    new_x2 = x_range[1]
    new_y1 = y_range[0]
    new_y2 = y_range[1]

    dist1 = sqrt(((new_x1 - point[0]) ** 2) + (new_y1 - point[1]) ** 2)
    dist2 = sqrt(((new_x2 - point[0]) ** 2) + (new_y2 - point[1]) ** 2)
    ret = [(dist1, (new_x1, new_y1)), (dist2, (new_x2, new_y2))]

    if x_range[0] <= point[0] <= x_range[1]:
        # print("    Point within x_range")
        # print("    Dist:", y_range[0] - point[1], x_range,  point[1])
        ret.append((abs(y_range[0] - point[1]), (point[0], y_range[0])))
    if y_range[0] <= point[1] <= y_range[1]:
        # print("    Point within y_range")
        # print("    Dist:", x_range[0] - point[0], y_range, point[0])
        ret.append((abs(x_range[0] - point[0]), (x_range[0], point[1])))

    ret = list(set(ret)) # Remove duplicate points
    # print("    Costs (", len(ret), "):", ret)
    return ret


def distance(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + (p2[1] - p1[1]) ** 2)


class AStarIterator:
    def __init__(self, mesh, source_point, destination_point, start_box, end_box):
        self.mesh = mesh
        self.source_point = source_point
        self.destination_point = destination_point
        self.start_box = start_box
        self.end_box = end_box

        self.h = []
        heappush(self.h, (0, 0, self.start_box, self.source_point))

        self.cost_so_far = dict()
        self.cost_so_far[self.source_point] = 0

        self.came_from = dict()
        self.came_from[self.start_box] = None

        self.pt_came_from = dict()
        self.pt_came_from[self.source_point] = None
        self.current_point = source_point

        self.points = dict()

    def iterate(self):
        obj = heappop(self.h)

        # print("\n------")
        # print("Popped: ", obj, end="", flush=True)

        current = obj[2]
        # print("<<< Left:", current[2], "Top:", current[0], "Height:", current[1] - current[0],
        #       "Width:", current[3] - current[2], ">>>")
        self.current_point = obj[3]

        if current == self.end_box:
            print("arrived at end box")
            self.pt_came_from[self.destination_point] = self.current_point
            self.cost_so_far[self.destination_point] = obj[0]
            self.points[self.destination_point] = (self.destination_point, self.end_box)
            return False

        neighbors = list(dict.fromkeys(self.mesh['adj'][current]))
        # print(f"Neighbors ({len(neighbors)}):")
        for nxt in neighbors:
            # print("\nnxt:", nxt, "<<< Left:", nxt[2], "Top:", nxt[0], "Height:", nxt[1] - nxt[0],
            #       "Width:", nxt[3] - nxt[2], ">>>")
            pts = find_least_dist_to_box(current, nxt, self.current_point)
            for p in pts:
                dist, point = p[0], p[1]
                if point != self.current_point:
                    new_cost = self.cost_so_far[self.current_point] + dist
                    if nxt not in self.came_from or point not in self.pt_came_from or new_cost < self.cost_so_far[point]:
                        self.cost_so_far[point] = new_cost
                        priority = new_cost + distance(point, self.destination_point)
                        val = (priority, new_cost, nxt, point)
                        # print("         Pushing ", val)
                        heappush(self.h, val)
                        self.came_from[nxt] = current
                        self.points[point] = (point, current)
                        self.pt_came_from[point] = self.current_point

        return True

    def finalize_paths(self):
        path = []
        boxes = {}
        ptr = self.destination_point

        while ptr is not self.source_point:
            path.append(self.points[ptr][0])
            boxes[self.points[ptr][1]] = self.points[ptr][1]
            ptr1 = ptr
            ptr = self.pt_came_from[ptr]
            if ptr == ptr1:
                print("WE HAVE A CYCLE:", ptr1, ptr)
                return None, None, 0
        path.append(self.source_point)

        cost = 0
        i = 0
        while i < len(path) - 1:
            cost = cost + distance(path[i], path[i + 1])
            i = i + 1

        return path, boxes, cost
