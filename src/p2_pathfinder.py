from heapq import heappop, heappushfrom math import sqrtdef find_path (source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    path = []    boxes = {}    print("===========================================================================")    print(f'Going from {source_point} to {destination_point}')    key_boxes = find_boxes(source_point, destination_point, mesh)    print(f'key boxes is {key_boxes}')    start_box = key_boxes['start']    end_box = key_boxes['end']    h = []    heappush(h, (0, start_box, source_point, destination_point))    heappush(h, (0, end_box, destination_point, source_point))    cost_so_far = dict()    cost_so_far[source_point] = 0    cost_so_far_backwords = dict()    cost_so_far_backwords[destination_point] = 0    points = dict()    pt_came_from = dict()    pt_came_from[source_point] = None    pt_came_from_backwords = dict()    pt_came_from_backwords[destination_point] = None    cost_direction = {destination_point: cost_so_far, source_point: cost_so_far_backwords}    came_from_direction = {destination_point: pt_came_from, source_point: pt_came_from_backwords}    common_point = None    while not h == []:        obj = heappop(h)        # print("------")        # print(f"Popped: ", obj)        current = obj[1]        # print("    Left:", current[2], "Top:", current[0], "Height:", current[1] - current[0],        #       "Width:", current[3] - current[2])        current_point = obj[2]        current_goal = obj[3]        if current_point in came_from_direction[source_point] and current_point in came_from_direction[destination_point]:            # pt_came_from[destination_point] = current_point            # cost_so_far[destination_point] = obj[0] + distance(destination_point, current_point)            common_point = current_point            break        neighbors = list(dict.fromkeys(mesh['adj'][current]))        for nxt in neighbors:            pts = find_least_dist_to_box(current, nxt, current_point)            # print("nxt:", nxt, "pts:", pts)            # print("    Left:", nxt[2], "Top:", nxt[0], "Height:", nxt[1] - nxt[0],            #       "Width:", nxt[3] - nxt[2])            for p in pts:                dist, point = p[0], p[1]                if point != current_point:                    new_cost = cost_direction[current_goal][current_point] + dist                    if point not in came_from_direction[current_goal] or new_cost < cost_direction[current_goal][point]:                        cost_direction[current_goal][point] = new_cost                        priority = new_cost + distance(point, current_goal)                        heappush(h, (priority, nxt, point, current_goal))                        points[point] = (point, current)                        came_from_direction[current_goal][point] = current_point    print("Finished computation")    source_ptr = common_point    destination_ptr = common_point    while source_ptr is not source_point:        boxes[points[source_ptr][1]] = 1        path.append(points[source_ptr][0])        source_ptr = came_from_direction[destination_point][source_ptr]    while destination_ptr is not destination_point:        boxes[points[destination_ptr][1]] = 1        path.insert(0, points[destination_ptr][0])        destination_ptr = came_from_direction[source_point][destination_ptr]    path.append(source_point)    path.insert(0,destination_point)    print(f'Path  {path}, {len(path)}')    # print("Cost:", cost_so_far[destination_point])    print(f'path of boxes is {boxes}')    cost = 0    i = 0    while i < len(path) - 1:        cost = cost + distance(path[i], path[i+1])        i  = i + 1    print("Point Cost:", cost)    return path, boxes.keys()def find_boxes(start, end, mesh):    boxes = {}    for box in mesh['boxes']:        if box[1] >= start[0] >= box[0]:            if box[3] >= start[1] >= box[2]:                print(f'found start box, {start} in {box}')                boxes['start'] = box        if box[1] >= end[0] >= box[0]:            if box[3] >= end[1] >= box[2]:                print(f'found end box, {end} in {box}')                boxes['end'] = box    return boxesdef find_least_dist_to_box(b1, b2, point):    x_range = [max(b1[0], b2[0]), min(b1[1], b2[1])]    y_range = [max(b1[2], b2[2]), min(b1[3], b2[3])]    # print(b1, b2, point)    # print("    x_range:", x_range, "y_range:", y_range)    #    # if b1[3] == b2[2]:    #     print("    Right neighbor")    # elif b1[2] == b2[3]:    #     print("    Left neighbor")    # elif b1[1] == b2[0]:    #     print("    Bottom neighbor")    # elif b1[0] == b2[1]:    #     print("    Top neighbor")    new_x1 = x_range[0]    new_x2 = x_range[1]    new_y1 = y_range[0]    new_y2 = y_range[1]    dist1 = sqrt(((new_x1 - point[0]) ** 2) + (new_y1 - point[1]) ** 2)    dist2 = sqrt(((new_x2 - point[0]) ** 2) + (new_y2 - point[1]) ** 2)    ret = [(dist1, (new_x1, new_y1)), (dist2, (new_x2, new_y2))]    if x_range[0] <= point[0] <= x_range[1]:        # print("    Point within x_range")        # print("    Dist:", y_range[0] - point[1], x_range,  point[1])        ret.append((abs(y_range[0] - point[1]), (point[0], y_range[0])))    if y_range[0] <= point[1] <= y_range[1]:        # print("    Point within y_range")        # print("    Dist:", x_range[0] - point[0], y_range, point[0])        ret.append((abs(x_range[0] - point[0]), (x_range[0], point[1])))    return retdef distance(p1, p2):    return sqrt(((p2[0] - p1[0]) ** 2) + (p2[1] - p1[1]) ** 2)