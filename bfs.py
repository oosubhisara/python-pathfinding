from map import *

DIRS = [ CellPos(-1, 0), CellPos(1, 0), CellPos(0, -1), CellPos(0, 1) ]

class PathNode:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.prev = None
        self.walkable = True

class Bfs:
    def __init__(self, path_map, row_count, col_count):
        self.path_map = path_map
        self.row_count = row_count
        self.col_count = col_count
        self.queue = []

    def find_path(self, start, end):
        self.queue = []
        start_node = self.path_map[start.row][start.col]
        start_node.visited = True
        self.queue.append(start_node)

        while len(self.queue) > 0:
            node = self.queue.pop(0)
            self.enqueue_neighbors(node)
            print("queue size: {0}".format(len(self.queue)))

        # Reconstruct path
        print("Reconstructing path...")
        path = []
        node = self.path_map[end.row][end.col].prev
        while node is not None and node.prev is not None:
            path.append(node)
            node = node.prev

        path.reverse()

        return path


    def enqueue_neighbors(self, path_node):
        for i in range(4):
            new_row = path_node.row + DIRS[i].row
            new_col = path_node.col + DIRS[i].col
            if new_row < 0 or new_row >= self.row_count \
                    or new_col < 0 or new_col >= self.col_count:
                continue

            nb = self.path_map[new_row][new_col]
            if not nb.visited and nb.walkable:
                nb.visited = True
                nb.prev = path_node 
                self.queue.append(nb)


