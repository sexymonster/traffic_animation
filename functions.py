from road_object import *

def set_link_data(Net, Links):

    for link in Links:
        data = link.attrib
        A = Link()
        A.id = data['id']
        A.type = data['type']
        A.num_lane = int(data['num_lane'])
        A.num_sect = int(data['num_sect'])
        A.ffspeed = int(data['ffspeed'])
        # A.max_spd = int(data['max_spd'])
        A.max_spd = data['max_spd']
        # A.min_spd = int(temp1[13])
        A.min_spd = data['min_spd']

        #adjusting scale for drawing
        A.length = int(data['length'])
        A.width = int(data['width']) * 15

        A.qmax = int(data['qmax'])
        A.waveSpd = int(data['waveSpd'])
        A.maxVeh = int(data['maxVeh'])

        A.from_node = int(data['fromNode'])
        A.to_node = int(data['toNode'])

        Net.Links[A.id] = A


def set_node_data(Net, Nodes):

    for node in Nodes:
        A = Node()
        data = node.attrib

        A.id = int(data['id'])
        A.type = data['type']
        A.num_port = data['num_port']

        for port in node.iter('port'):
            p_data = port.attrib
            P = Port(Net.Links[p_data['link_id']])
            P.direction = int(p_data['direction'])
            P.type = p_data['type']
            A.ports.append(P)

        # connection data
        if A.type == 'intersection':

            A.num_connection = data['num_connection']
            # for connection in node.iter('connection'):
            #     print(connection.attrib)
            #     # for j in range(len(c_temp1) - 1):
            #     #     con = Connection()
            #     #     con.id = c_data[1]
            #     #     con.from_link = c_data[3]
            #     #     con.from_lane = c_data[5]
            #     #     con.to_link = c_data[7]
            #     #     con.to_lane = c_data[9]
            #     #     con.length = c_data[11]
            #     #     # con.priority = c_data[13]
            #     #     A.connections.append(con)
        A.set_width_and_height()
        Net.Nodes[A.id] = A

    for i in range(len(Net.Nodes)):
        for j in range(len(Net.Nodes[i].ports)):
            idx = Net.Nodes[i].ports[j].link.to_node
            Net.Nodes[i].ports[j].connected_node = Net.Nodes[idx]


def set_station_data(Net, Stations):

    for station in Stations:

        A = Station()
        s_data = station.attrib
        A.id = s_data['id']
        A.link_ref = s_data['link_ref']
        A.lane_ref = s_data['lane_ref']
        A.pos = int(s_data['pos'])
        Net.Stations[A.id] = A

def set_cell_data(Net,C_data):

    for link in C_data.iter('link'):
        for lane in link.iter('lane'):
            a_lane = dict()
            for cell in lane.iter('cell'):
                C = Cell(cell.attrib)
                a_lane[cell.attrib['id']] = C

            Net.Links[link.attrib['id']].lanes[lane.attrib['id']] = a_lane

def set_meso_data(messo,timeline,Network):

    for cell in messo.iter('Cell'):
        ms_data = cell.attrib
        if not ms_data['timestep'] in timeline.keys():
            # print('o')
            timeline[ms_data['timestep']] = []

        rect = Network.Links[ms_data['link_id']].lanes[ms_data['lane_id']][ms_data['id']].rect
        data = [rect, ms_data['spd'], ms_data['icf']]
        timeline[ms_data['timestep']].append(data)
        # print(rect)
        # timeline[ms_data['timestep']].append([ms_data['spd']])
        # print(ms_data)

    # print(list(timeline.values()))


def set_vehicles(Vehicles):
    pass