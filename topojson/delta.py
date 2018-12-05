# coding: utf-8

def delta_encode(coordinates):

    x0, y0 = coordinates[0]
    delta_coords = [[ x0, y0 ]]

    for x, y in coordinates[1:]:

        if not (x == x0 and y == y0):
            delta_coords.append([ x - x0, y - y0 ])
            x0 = x
            y0 = y
    
    if len(delta_coords) == 1:
        delta_coords.append([ 0, 0 ])

    return delta_coords

def delta_decode(delta_coords):

    x, y = delta_coords[0]
    coordinates = [[ x, y ]]

    for dx, dy in delta_coords[1:]:
        x = x + dx
        y = y + dy
        coordinates.append([ x, y ])

    return coordinates