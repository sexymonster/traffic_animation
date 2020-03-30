class Network:
    def __init__(self):
        self.id = 0
        self.Links = dict()
        self.Nodes = dict()
        self.Stations = dict()

    def print_links(self):
        for i in range(len(self.Links)):
            print('Link number', i)
            print(self.Links[i])

    #for debugging
    def print_nodes(self):
        for i in range(len(self.Nodes)):
            print('Node number', i)
            print(self.Nodes[i])

            # if len(self.Nodes[i].ports)>1:
            print('port data')
            for j in range(len(self.Nodes[i].ports)):
                print(self.Nodes[i].ports[j])

            if len(self.Nodes[i].connections) > 1:
                print('connection data')
                for j in range(len(self.Nodes[i].connections)):
                    print(self.Nodes[i].connections[j])

    def print_stations(self):
        pass


class Node:
    def __init__(self):
        self.id = None
        # 0 for intersection, 1 for terminals
        self.type = None
        self.num_port = 0
        self.num_connection = None
        self.ports = []
        self.connections = []
        self.width = 0
        self.height = 0

        #for drawing
        self.coord = None
        self.on_canvas = False

    def is_on_canvas(self):
        return self.on_canvas

    def __str__(self):
        return str(self.id) + str(self.type) + str(self.num_port) + str(self.num_connection)

    def set_width_and_height(self):
        width = 0

        for i in range(len(self.ports)):
            if self.ports[i].direction == 0:
                width += self.ports[i].link.width
            elif self.ports[i].direction == 180:
                width += self.ports[i].link.width

        height = 0
        for i in range(len(self.ports)):
            if self.ports[i].direction == 270:
                height += self.ports[i].link.width
            elif self.ports[i].direction == 90:
                height += self.ports[i].link.width

        if self.type == 'terminal':
            width *= 2
            height *= 2

        self.width = width/2
        self.height = height/2


class Link:
    def __init__(self):
        self.id = None
        # 0 for straight
        self.type = None
        self.num_lane = 0
        self.num_sect = 0
        self.ffspeed = 0
        self.max_spd = 0
        self.min_spd = 0
        self.length = 0
        self.width = 0
        self.qmax = 0
        self.waveSpd = 0
        self.maxVeh = 0
        self.from_node = None
        self.to_node = None

        # for drawing
        self.lanes = dict()
        self.on_canvas = False

        self.station = None

    def is_on_canvas(self):
        return self.on_canvas


    #for debugging
    def __str__(self):
        return str(self.id) + str(self.type) + str(self.num_lane) + '...' + str(self.maxVeh)


class Cell:
    def __init__(self,attrib):
        self.id = attrib['id']
        self.offset = int(attrib['offset'])
        self.length = int(attrib['length'])
        self.rect = None

        self.start_point = None
        self.end_point = None

    def __str__(self):
        return str(self.id) + ',' +  str(self.offset) + ',' + str(self.length)

class Connection:
    def __init__(self):
        self.id = None
        self.from_link = None
        self.from_lane = None
        self.to_link = None
        self.to_lane = None
        self.length = 0
        self.priority = None

    def __str__(self):
        return self.from_link + "," + self.from_lane

class Station:
    def __init__(self):
        self.id = None
        self.link_ref = None
        self.lane_ref = None
        self.pos = None
        self.rect = None

    def __str__(self):
        return self.id + "," + self.link_ref + "," + self.lane_ref

class Port:
    def __init__(self, Link):
        self.link = Link
        self.direction = 0
        # 0 for out, 1 for in
        self.type = None
        self.connected_node = None

    def __str__(self):
        return 'link:' + str(self.link) + ", port:" + str(self.direction) + str(self.type) + ", connected_node: " + str(self.connected_node)

    def set_station_pos(self):
        pass


class Phase:
    def __init__(self):
        pass

