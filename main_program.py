#Created by fierylion. On 09/10/2022
#Please install pyinputplus module by AI SWEGART
import curses
import time, pyinputplus as pyip
from queue import Queue
from graphs import Graph
from maze_generator import square_maze
import copy
from curses import wrapper
class maze():
    def __init__(self):
        #Necessary data to form the maze
         self.size = pyip.inputInt(prompt="Enter the number size of the maze: ")
         self.maz = square_maze(self.size).generate()
         table = list(copy.deepcopy(self.maz))
         idx = 0
         coordinates = {}
         for y in range(len(table)):
             for x in range(len(table[0])):
                 if table[y][x] == " ":
                     table[y][x] = str(idx)
                     coordinates[idx] = (y, x)
                     idx+=1
         table_display = ""
         for row in table:
             table_display+=("   ".join(row) + "\n")
         print(table_display)

         self.source= pyip.inputInt(prompt="Enter the source coordinate: ")
         self.source = coordinates[self.source]
         self.destination= pyip.inputInt(prompt="Enter the destination coordinate: ")
         self.destination = coordinates[self.destination]
         self.algo_choice = pyip.inputMenu(prompt="Please enter the search algorithm to be performed: \n", choices=["BREADTH FIRST SEARCH", "DEPTH FIRST SEARCH"], numbered=True)
         self.run()
    def run(self):
        choice = self.algo_choice

        if choice == "BREADTH FIRST SEARCH":
            try:
                self.maze_finder_bfs(self.maz)
            except KeyError:
                print("Enter a valid coordinate: ")
            except:
                print("Please expand your screen or reduce maze size: ")
        elif choice == "DEPTH FIRST SEARCH":
            try:
                self.maze_finder_dfs(self.maz)
            except KeyError:
                print("Enter a valid coordinate: ")
            except:
                print("Please expand your screen or reduce maze size: ")

    def edges_maker(self, matrix):
        edges = []
        col_length = len(matrix[0]) # The number of columns is the same for each row
        row_length = len(matrix)
        # iterate over the matrix to obtain the nodes
        for row in range(row_length):
            for col in range(col_length):
                if matrix[row][col] == " ":  # check if it isn't an obstacle
                    if col < col_length - 1:
                        # check for right
                        if matrix[row][col + 1] == " ":
                            edges.append(((row, col), (row, col + 1)))
                    if row < row_length - 1:
                        # check for bottom
                        if matrix[row + 1][col] == " ":
                            edges.append(((row, col), (row + 1, col)))
        return edges
    #return a hash_map of each node to their repective index i.e {(row, col): 0}
    def node_index(self, edges):
        index_to_edge = {}
        idx = 0  # Assing index to each node
        for n1, n2 in edges:
            if n1 not in index_to_edge:
                index_to_edge[n1] = idx
                idx += 1
            if n2 not in index_to_edge:
                index_to_edge[n2] = idx
                idx += 1
        return index_to_edge

    #reverse of node_index method. The return map; maps index to its respective node
    def index_node(self, edges):
        index_to_edge = {}
        idx = 0
        for n1, n2 in edges:
            if n1 not in index_to_edge.values():
                index_to_edge[idx] = n1
                idx += 1
            if n2 not in index_to_edge.values():
                index_to_edge[idx] = n2
                idx += 1
        return index_to_edge
    #create abstract edges which can be understood by the graph class, edge_map is data from node_index method.
    def index_edge(self, edges, edge_map):
        abstract_edges = []
        for n1, n2 in edges: #node n1 and n2
            abstract_edges.append((edge_map[n1], edge_map[n2]))
        num_of_nodes = max(edge_map.values())
        print(num_of_nodes)
        return ((num_of_nodes + 1, abstract_edges))
    def maze_finder_bfs(self, maz):
        def maze_finder(stdscr):
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            BLACK_BLUE = curses.color_pair(1)
            BLACK_RED = curses.color_pair(2)
            edges = maze.edges_maker(self, maz)  #all edges that arent in abstract form
            node_ind = maze.node_index(self, edges)
            ind_node = maze.index_node(self, edges)
            graph_nodes = maze.index_edge(self, edges, node_ind)
            maze_graph = Graph(*graph_nodes)  #A graph presenting all the nodes in the matrix ---> Graph(*graph_nodes, True)-->print(maze_graph)
            source = node_ind[self.source]
            q1 = Queue()      #queue is used in breadth first search
            visited = []
            parent = [None]*len(maze_graph.data)  #parent to enable back_tracking
            destination_found = False
            if source < len(maze_graph.data):
                q1.put(source)
                visited.append(source)
            while not q1.empty():
                element = q1.get()
                vis_node = ind_node[element]  #map index back to node
                maz[vis_node[0]][vis_node[1]] = "*"  if element != source else "S"   #visited node
                if vis_node == self.destination:    # we found the destination
                    maz[vis_node[0]][vis_node[1]] = "D"
                    destination_found = True
                string_maze = ""
                for elm in maz:
                    string_maze += (" ".join(elm) + "\n")
                stdscr.addstr(2, 0, string_maze, BLACK_RED)
                stdscr.refresh()
                time.sleep(0.1)
                if destination_found:
                    break
                for node in maze_graph.data[element]:
                    if node not in visited:
                        parent[node] = element
                        visited.append(node)
                        q1.put(node)
            if destination_found:
                stdscr.refresh()
                stdscr.addstr(0, 0, "   BACK_TRACKING", BLACK_BLUE)
                curr = parent[node_ind[self.destination]]
                while parent[curr] != None:
                    p_ind = ind_node[curr]
                    maz[p_ind[0]][p_ind[1]] = "B"
                    string_maze = ""
                    for elm in maz:
                        string_maze += (" ".join(elm) + "\n")
                    stdscr.refresh()
                    stdscr.addstr(2, 0, string_maze, BLACK_BLUE|curses.A_REVERSE)
                    time.sleep(0.4)
                    curr = parent[curr]
                h, w = stdscr.getmaxyx()
                stdscr.addstr(h - 2, w - 1, "   PRESS ANY KEY", BLACK_BLUE)
                stdscr.getch()
            else:
                h, w = stdscr.getmaxyx()
                stdscr.addstr(h - 2, w - 1, "   NOT FOUND: PRESS ANY KEY", BLACK_RED)
                stdscr.getch()
        wrapper(maze_finder)

    def maze_finder_dfs(self, maz):
        def maze_finder(stdscr):
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            BLACK_BLUE = curses.color_pair(1)
            BLACK_RED = curses.color_pair(2)
            edges = maze.edges_maker(self, maz)  # all edges that arent in abstract form
            node_ind = maze.node_index(self, edges)
            ind_node = maze.index_node(self, edges)
            graph_nodes = maze.index_edge(self, edges, node_ind)
            maze_graph = Graph(*graph_nodes)  # A graph presenting all the nodes in the matrix ---> Graph(*graph_nodes, True)-->print(maze_graph)
            source = node_ind[self.source]
            destination_found = False
            stack = []
            parent = [None] * len(maze_graph.data)
            visited = [False] * len(maze_graph.data)
            if source < len(maze_graph.data):
                stack.append(source)
            while len(stack)>0:
                element = stack.pop()
                if not visited[element]:
                    visited[element] = True
                    vis_node = ind_node[element]
                    maz[vis_node[0]][vis_node[1]] = "*"  if element != source else "S" # visited node
                    if vis_node == self.destination:  # we found the destination
                        maz[vis_node[0]][vis_node[1]] = "D"
                        destination_found = True
                    string_maze = ""
                    for elm in maz:
                        string_maze += (" ".join(elm) + "\n")
                    stdscr.addstr(2, 0, string_maze, BLACK_RED)
                    stdscr.refresh()
                    time.sleep(0.4)
                    if destination_found:
                        break
                    for node in maze_graph.data[element]:
                        if not visited[node]:
                            stack.append(node)
                            parent[node] = element
            if destination_found:
                stdscr.refresh()
                stdscr.addstr(0, 0, "   BACK_TRACKING", BLACK_BLUE)
                curr = parent[node_ind[self.destination]]
                while parent[curr] != None:
                    p_ind = ind_node[curr]
                    maz[p_ind[0]][p_ind[1]] = "B"
                    string_maze = ""
                    for elm in maz:
                        string_maze += (" ".join(elm) + "\n")
                    stdscr.refresh()
                    stdscr.addstr(2, 0, string_maze, BLACK_BLUE | curses.A_REVERSE)
                    time.sleep(0.4)
                    curr = parent[curr]
                h, w = stdscr.getmaxyx()
                stdscr.addstr(h - 2, w - 1, "   PRESS ANY KEY", BLACK_BLUE)
                stdscr.getch()
            else:
                h, w = stdscr.getmaxyx()
                stdscr.addstr(h - 2, w - 1, "   NOT FOUND: PRESS ANY KEY", BLACK_RED)
                stdscr.getch()

        wrapper(maze_finder)
maze()

