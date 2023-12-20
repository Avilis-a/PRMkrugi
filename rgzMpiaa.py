from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
import random
import math
import networkx as nx
import sys


maxCoordX = 600
maxCoordY = 700
mas = []
obstacles = []
start = []
end = []



def MinNode(graph, currentNode):
    dist = 10000
    minNode = None
    for node in graph.nodes():
        if Distance(node, currentNode) < dist:
            minNode = node
            dist = Distance(node, currentNode)
    return minNode



def GetNearNodes(graph, currentNode, dist):
    nodes = []
    for node in graph.nodes():
        if Distance(node, currentNode) < dist:
            nodes.append(node)
    return nodes



def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    def on_segment(px, py, qx, qy, rx, ry):
        if (qx <= max(px, rx) and qx >= min(px, rx) and
                max(py, ry) >= qy >= min(py, ry)):
            return True
        return False

    def orientation(px, py, qx, qy, rx, ry):
        val = (qy - py) * (rx - qx) - (qx - px) * (ry - qy)
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    o1 = orientation(x1, y1, x2, y2, x3, y3)
    o2 = orientation(x1, y1, x2, y2, x4, y4)
    o3 = orientation(x3, y3, x4, y4, x1, y1)
    o4 = orientation(x3, y3, x4, y4, x2, y2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(x1, y1, x3, y3, x2, y2):
        return True

    if o2 == 0 and on_segment(x1, y1, x4, y4, x2, y2):
        return True

    if o3 == 0 and on_segment(x3, y3, x1, y1, x4, y4):
        return True

    if o4 == 0 and on_segment(x3, y3, x2, y2, x4, y4):
        return True

    return False


def Colides(obstacles, node1, node2):
    for obstacle in obstacles:

        if Distance(obstacle[0], node1) <= obstacle[1] + obstacle[1] / 10:
            return True

        t = (node1[0] * (node1[0] - node2[0]) + node1[1] * (node1[1] - node2[1]) -
             obstacle[0][0] * (node1[0] - node2[0]) - obstacle[0][1] * (
            node1[1] - node2[1])) / (0 - (node1[1] - node2[1]) ** 2 -
                                     (node1[0] - node2[0]) ** 2)
        node = ((node1[0] + t * (node1[0] - node2[0])), (node1[1] +
                                                         t * (node1[1] - node2[1])))

        if (line_intersection(obstacle[0][0], obstacle[0][1], node[0],
                              node[1], node2[0], node2[1], node1[0], node1[1])
                or line_intersection(obstacle[0][0], obstacle[0][1], node[0] + 0.5, node[1] + 0.5,
                                     node2[0], node2[1], node1[0], node1[1])
                or line_intersection(obstacle[0][0], obstacle[0][1], node[0] - 0.5, node[1] - 0.5,
                                     node2[0], node2[1], node1[0], node1[1])) \
                and Distance(node, obstacle[0]) <= obstacle[1] + obstacle[1] / 100:
            return True
    return False



def PRM(maxIt, k):

    for obstacle in obstacles:
        if Distance(obstacle[0], start) <= obstacle[1] or Distance(obstacle[0], end) <= obstacle[1]:
            return None

    g = nx.Graph()
    st = (start[0], start[1])
    en = (end[0], end[1])
    g.add_node(en)
    g.add_node(st)


    for _ in range(maxIt):
        currentNode = (random.randint(10, maxCoordX - 10),
                       random.randint(10, maxCoordY - 10))


        for _ in range(2):
            for obstacle in obstacles:
                minNode = MinNode(g, currentNode)
                t = 0.01
                node = currentNode
                while Distance(obstacle[0], currentNode) <= obstacle[1] + 10:
                    currentNode = ((node[0] - t * (node[0] - minNode[0])),
                                (node[1] - t * (node[1] - minNode[1])))
                    t = t + 0.01
        g.add_node(currentNode)

    fSt = False
    fEn = False
    for node in g.nodes():
        near = GetNearNodes(g, node, k)
        for n in near:
            if node != n and not Colides(obstacles, node, n):
                if node == en:
                    fEn = True
                if node == st:
                    fSt = True
                g.add_edge(node, n, weight=Distance(node, n))
    if not fSt or not fEn:
        return None
    return g



def Distance(node1, node2):
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)



def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.nodes())


    shortest_path = {}


    previous_nodes = {}

    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value

    shortest_path[start_node] = 0

    while unvisited_nodes:

        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbors = graph.neighbors(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.get_edge_data(current_min_node, neighbor)[
                "weight"]
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value

                previous_nodes[neighbor] = current_min_node

        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path



def get_result(previous_nodes, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    path.append(start_node)
    path.reverse()
    return path



def draw_edges():
    maxIt = int(entry.get())
    k = int(entry1.get())

    graph = PRM(maxIt, k)
    if graph is None:
        mb.showinfo("Маршрут", "нет пути")
    else:
        previous_nodes, shortest_path = dijkstra_algorithm(
            graph, (start[0], start[1]))
        if shortest_path[(end[0], end[1])] == sys.maxsize:
            mb.showinfo("Маршрут", "нет пути")
        else:
            path = get_result(
                previous_nodes, (start[0], start[1]), (end[0], end[1]))
            for u, v in graph.edges():
                canvas.create_line(u[0], u[1], v[0], v[1], tags="cc")
                canvas.create_oval(u[0] - 3, u[1] - 3, u[0] +
                                   3, u[1] + 3, fill="yellow", tags="cc")
                canvas.create_oval(v[0] - 3, v[1] - 3, v[0] +
                                   3, v[1] + 3, fill="yellow", tags="cc")
            canvas.create_oval(start[0] - 3, start[1] - 3,
                               start[0] + 3, start[1] + 3, fill="red")
            canvas.create_oval(end[0] - 3, end[1] - 3,
                               end[0] + 3, end[1] + 3, fill="purple")
            

            for i in range(len(path) - 1):
                node1 = path[i]
                node2 = path[i + 1]
                canvas.create_line(node1[0], node1[1],
                                   node2[0], node2[1], fill="green", width=4, tags="cc")
                

            mb.showinfo("Маршрут", "Найден следующий лучший маршрут {}.".format(
                shortest_path[(end[0], end[1])]))



def save_scene():
    file = open("PRM.txt", "w")
    file.write("start, end:\n" + str(start) + '\n' +
               str(end) + '\n' + "obstracles:\n")
    for obstacle in obstacles:
        file.write(str(obstacle) + '\n')
    file.close()



def load_scene():
    file = open("PRM.txt")
    canvas.delete("all")
    obstacles.clear()
    start.clear()
    end.clear()
    f_start = False
    f_end = False
    for line in file:
        if line != "start, end:\n" and line != "obstracles:\n":
            if not f_start:
                l = line.split(", ")
                start.append(float(l[0][1:]))
                start.append(float(l[1][:len(l[1]) - 2]))
                f_start = True
            elif not f_end:
                l = line.split(", ")
                end.append(float(l[0][1:]))
                end.append(float(l[1][:len(l[1]) - 2]))
                f_end = True
            else:
                l = line.split("), ")
                l1 = l[0].split(", ")
                obstacles.append(
                    ((float(l1[0][2:]), float(l1[1])), float(l[1][:len(l[1]) - 2])))
    canvas.create_oval(start[0] - 3, start[1] - 3,
                       start[0] + 3, start[1] + 3, fill="yellow")
    canvas.create_oval(end[0] - 3, end[1] - 3, end[0] + 3,
                       end[1] + 3, fill="green")
    for obstacle in obstacles:
        canvas.create_oval(obstacle[0][0] - obstacle[1], obstacle[0][1] - obstacle[1], obstacle[0][0] + obstacle[1],
                           obstacle[0][1] + obstacle[1], fill="red")



def clear_scene():
    canvas.delete("all")
    start.clear()
    end.clear()
    obstacles.clear()


def delete_graph():
    canvas.delete("cc")



root = Tk()
root.title("PRM")
root.geometry(f'{maxCoordX + 200}x{maxCoordY + 10}')


entry = ttk.Entry()
entry.place(x=maxCoordX + 10, y=maxCoordY - 500, width=180, height=40)
entry.insert(0, "Введите количество итераций")

entry1 = ttk.Entry()
entry1.place(x=maxCoordX + 50, y=maxCoordY - 600, width=120, height=40)
entry1.insert(0, "Введите радиус")


canvas = Canvas(bg="white", width=maxCoordX, height=maxCoordY)
canvas.pack(anchor="nw", expand=1)



btn = ttk.Button(text="Draw graph", command=draw_edges)
btn.place(x=maxCoordX + 50, y=maxCoordY - 400, width=120, height=40)
btn1 = ttk.Button(text="Save scene", command=save_scene)
btn1.place(x=maxCoordX + 50, y=maxCoordY - 300, width=120, height=40)
btn2 = ttk.Button(text="Load scene", command=load_scene)
btn2.place(x=maxCoordX + 50, y=maxCoordY - 200, width=120, height=40)
btn3 = ttk.Button(text="Clear scene", command=clear_scene)
btn3.place(x=maxCoordX + 50, y=maxCoordY - 100, width=120, height=40)
btn4 = ttk.Button(text="Delete graph", command=delete_graph)
btn4.place(x=maxCoordX + 50, y=maxCoordY - 700, width=120, height=40)


def add_conclusion_vertex(event):
    if len(start) == 0 or (len(start) != 0 and len(end) != 0):
        canvas.delete("cc")
        start.clear()
        end.clear()
        start.append(event.x)
        start.append(event.y)
        canvas.create_oval(event.x - 3, event.y - 3, event.x + 3,
                           event.y + 3, fill="yellow", tags="cc")
    elif len(end) == 0:
        canvas.create_oval(event.x - 3, event.y - 3, event.x +
                           3, event.y + 3, fill="green", tags="cc")
        end.append(event.x)
        end.append(event.y)



def add_obstacle(event):
    mas.append((event.x, event.y))


    if len(mas) == 2:
        center = (mas[0][0], mas[0][1])
        radius = Distance(center, (mas[1][0], mas[1][1]))
        canvas.create_oval(center[0] - radius, center[1] - radius,
                           center[0] + radius, center[1] + radius, fill="red")
        mas.clear()
        obstacles.append((center, radius))



canvas.bind('<Button-3>', add_conclusion_vertex)
canvas.bind('<Button-1>', add_obstacle)

root.mainloop()
