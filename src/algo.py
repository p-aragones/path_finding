from src.cell import *

def get_path(start, end, surface, window): #compute and print path from start to end
    
    global openList
    global closedList
    global path

    openList = []
    closedList = []
    path = []

    print("start:", start, "end", end)
    start_node = Cell(start[0], start[1])
    end_node = Cell(end[0], end[1])
    openList.append(start_node)
    current_node = openList[0]
    current_indx = 0
    while len(openList) > 0:
        current_node = openList[0]
        current_indx = 0
        for indx, item in enumerate(openList): #checks openList for available nodes
            if item.f < current_node.f: #node on the list has a better f value than current node
                current_node = item
                current_indx = indx
        openList.pop(current_indx) #delete current node from the open list
        closedList.append(current_node) #add current node to the closed list
        if current_node.position == end_node.position: #reached end cell - finished
            current = current_node
            while current is not None:
                path.append(current)
                grid[current.position[0]][current.position[1]].print_path(surface, window)
                current = current.parent
            return (path[::-1]) #inversed path
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # cells surrounding current node
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) -1) or node_position[1] < 0: #check grid bounds
                continue
            if grid[node_position[0]][node_position[1]].walkable == 0:
                continue
            if grid[node_position[0]][node_position[1]] in closedList:
                continue
            new_node = Cell(node_position[0], node_position[1], current_node)
            children.append(new_node)
        for child in children: #loops through children
            for closed_child in closedList:
                if child == closed_child: #child in the closed list
                    break
            else: #child not closed
                child.g = current_node.g + 1
                child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
                child.f = child.g + child.h
            for open_node in openList:
                if child == open_node and child.f >= open_node.f: #child in openList
                    break
            else:
                openList.append(child) #better node found