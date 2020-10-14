from heapq import heappop, heappushfrom math import sqrt, infdef find_path (source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    path = []    boxes = {}    print(f'Going from {source_point} to {destination_point}')    key_boxes = find_boxes(source_point, destination_point, mesh)    print(f'key boxes is {key_boxes}')    start_box = key_boxes['start']    end_box = key_boxes['end']    h = []    heappush(h, (0, start_box))    came_from = dict()    came_from[start_box] = None    cost_so_far = dict()    cost_so_far[start_box] = 0    lines = dict()    current_point = source_point    path.append(source_point)    while not h == []:        current_box = heappop(h)[1]        if current_box == end_box:            break        for adj_box in mesh['adj'][current_box]:            val = find_distance_boxes(current_box, adj_box, current_point)            current_point = val[1]            distance = val[0]            new_cost = cost_so_far[current_box] + distance            if adj_box not in cost_so_far or new_cost < cost_so_far[adj_box]:                cost_so_far[adj_box] = new_cost                priority = new_cost + find_distance_two_points(destination_point, current_point)                heappush(h, (priority, adj_box))                came_from[adj_box] = current_box    ptr = end_box    while ptr is not start_box:        boxes[ptr] = 1        ptr = came_from[ptr]    boxes[ptr] = 1    return path, boxes.keys()def find_boxes(start, end, mesh):    boxes = {}    for box in mesh['boxes']:        if box[1] >= start[0] >= box[0]:            if box[3] >= start[1] >= box[2]:                print(f'found start box, {start} in {box}')                boxes['start'] = box        if box[1] >= end[0] >= box[0]:            if box[3] >= end[1] >= box[2]:                print(f'found end box, {end} in {box}')                boxes['end'] = box    return boxesdef find_distance_boxes(b1, b2, point):    x_range = (max(b1[0], b2[0]), min(b1[1], b2[1]))    y_range = (max(b1[2], b2[2]), min(b1[3], b2[3]))    # print(f'point between b1:{b1} and b2:{b2} falls somewhere between x: {x_range} and y: {y_range}')    new_x = 0    new_y = 0    if point[0] not in range(x_range[0], x_range[1]):        if point[0] < x_range[0]:            new_x = x_range[0]        elif point[0] > x_range[1]:            new_x = x_range[1]    else:        new_x = point[0]    if point[1] not in range(y_range[0], y_range[1]):        if point[1] < y_range[0]:            new_y = y_range[0]        elif point[1] > y_range[1]:            new_y = y_range[1]    else:        new_y = point[1]    new_p = (new_x, new_y)    dist = sqrt(((point[0] - new_p[0]) ** 2) + ((point[1] - new_p[1]) ** 2))    obj = (dist, new_p)    return objdef find_distance_two_points(point, new_p):    return sqrt(((point[0] - new_p[0]) ** 2) + ((point[1] - new_p[1]) ** 2))