import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from road_object import *
from functions import *
import xml.etree.ElementTree as ET

#pyqt 5.14.1
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class Map(QGraphicsView):

    def __init__(self, parent):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        # draw tools

        # lines
        self.dot_line = QPen(QColor(0, 0, 0), 4, Qt.DotLine)
        self.dot_line2 = QPen(Qt.black, 1, Qt.DotLine)
        self.dash_dot_line = QPen(Qt.black, 4, Qt.DashDotLine)
        self.n_line = QPen(Qt.black, 5)

        # lane block
        self.pen = QPen(Qt.lightGray, 0.1)
        self.brush = QBrush(Qt.lightGray)

        # terminal block
        self.brush_source = QBrush(QColor(230,230,230))
        self.brush_sink = QBrush(QColor(30, 30, 30))

        self.count = 0
        self.timer = None
        self.t = None
        self.before = []

    def anime_1(self,acts,keys):
        # print(keys[self.count])
        self.t.setHtml(keys[self.count])
        # print(len(self.before))
        for act in self.before:
            act.setBrush(Qt.lightGray)

        self.scene.update()
        self.before = []

        # print(len(self.before))
        for act in acts:

            if act[1] == '-nan(ind)':
                continue
            elif act[1] == 'inf':
                act[0].setBrush(Qt.green)
                self.before.append(act[0])
            else:

                v = float(act[1])
                if v < 30:
                    act[0].setBrush(Qt.red)
                elif v < 60:
                    act[0].setBrush(Qt.yellow)
                else:
                    act[0].setBrush(Qt.darkGreen)
                self.before.append(act[0])

            self.scene.update()

        self.count += 1
        if self.count == len(keys):
            self.timer.stop()

    def meso_animation(self, timeline):

        keys = list(timeline.keys())
        first_time = keys[self.count]

        self.t = QGraphicsTextItem(first_time)
        self.t.setPos(-200,-200)
        font = self.t.font()
        font.setPointSize(20)
        font.setWeight(300)
        self.t.setFont(font)
        self.t.setTextWidth(400)
        self.scene.addItem(self.t)
        self.scene.update()

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(lambda :self.anime_1(timeline[keys[self.count]], keys))
        self.timer.start()

    def draw_network(self, Network):
        # drawing starts with non-terminal node object.
        coord = [0, 0, 0, 0]
        for i in range(len(Network.Nodes)):

            Node = Network.Nodes[i]

            if Node.type == 'terminal':
                continue
            else:
                break

        self.draw_node(Node,coord)
        self.draw_stations(Network)

    def draw_stations(self,Net):
        Stations = Net.Stations
        for i in range(1,len(Stations)+1):
            station = Stations['Stat' + str(i)]
            # print(Net.Links[station.link_ref].station)
            data = Net.Links[station.link_ref].station
            start_x = data[0]
            start_y = data[1]
            # print(station.id,start_x,start_y)
            if data[2] == 0:
                if data[3] == 'in':
                    A = QPointF(start_x, start_y+station.pos)
                    B = QPointF(start_x - 30, start_y+station.pos + 50)
                else:
                    A = QPointF(start_x, start_y - station.pos)
                    B = QPointF(start_x + 30, start_y - station.pos - 50)

            if data[2] == 90:
                if data[3] == 'in':
                    A = QPointF(start_x-station.pos, start_y)
                    B = QPointF(start_x-station.pos-50, start_y - 30)
                else:
                    A = QPointF(start_x + station.pos, start_y)
                    B = QPointF(start_x + station.pos + 50, start_y + 30)

            if data[2] == 180:
                if data[3] == 'in':
                    A = QPointF(start_x, start_y-station.pos)
                    B = QPointF(start_x + 30, start_y-station.pos -50)
                else:
                    A = QPointF(start_x, start_y + station.pos)
                    B = QPointF(start_x - 30, start_y + station.pos + 50)

            if data[2] == 270:
                if data[3] == 'in':
                    A = QPointF(start_x+station.pos, start_y)
                    B = QPointF(start_x+station.pos + 50, start_y +30)
                else:
                    A = QPointF(start_x - station.pos, start_y)
                    B = QPointF(start_x - station.pos - 50, start_y - 30)

            rect = QRectF(A, B)
            item = self.scene.addRect(rect, self.n_line, self.brush_source)
            item.setToolTip(station.id)
            station.rect = item




    def draw_node(self, Node, coord):
        # draw nodes

        if not Node.on_canvas:
            Node.on_canvas = True
            # print(Node.id, coord, "draw start")

            if Node.type == 'terminal':
                # draw terminal(source for white, sink for black)

                if (coord[2]-coord[0]) > 45:
                    mid = coord[2]-(coord[2]-coord[0])/2
                    A = QPointF(coord[0], coord[1])
                    B = QPointF(mid, coord[3])
                    C = QPointF(coord[2],coord[1])

                    rect1 = QRectF(A, B)
                    rect2 = QRectF(B, C)

                    if Node.ports[0].direction == 180:
                        item1 = self.scene.addRect(rect1, self.n_line, self.brush_source)
                        item2 = self.scene.addRect(rect2, self.n_line, self.brush_sink)

                    else:
                        item1 = self.scene.addRect(rect1, self.n_line, self.brush_sink)
                        item2 = self.scene.addRect(rect2, self.n_line, self.brush_source)


                else:
                    mid = coord[3] - (coord[3] - coord[1]) / 2
                    A = QPointF(coord[0], coord[1])
                    B = QPointF(coord[2], mid)
                    C = QPointF(coord[0], coord[3])

                    rect1 = QRectF(A, B)
                    rect2 = QRectF(B,C)

                    if Node.ports[0].direction == 270:
                        item1 = self.scene.addRect(rect1, self.n_line, self.brush_source)
                        item2 = self.scene.addRect(rect2, self.n_line, self.brush_sink)

                    else:
                        item1 = self.scene.addRect(rect1, self.n_line, self.brush_sink)
                        item2 = self.scene.addRect(rect2, self.n_line, self.brush_source)

                item1.setZValue(50)
                item1.setToolTip(str(Node.id))
                item2.setZValue(50)
                item2.setToolTip(str(Node.id))

                Node.on_canvas = True
                # print(Node.id, coord, "end")
                return

            for j in range(len(Node.ports)):

                # Adjusting coord to draw connected links
                # and expand using link information.

                port = Node.ports[j]
                # print(Node.id, "draw", port.link.id)

                if port.type == "out":

                    if port.direction == 270:
                        coord[3] += port.link.width

                        A = QPointF(coord[0], coord[1])
                        B = QPointF(coord[2] - port.link.length, coord[3])

                        self.expanding(port, coord)

                    elif port.direction == 180:
                        coord[2] += port.link.width

                        A = QPointF(coord[0], coord[3])
                        B = QPointF(coord[2], coord[3] + port.link.length)

                        self.expanding(port,coord)


                    elif port.direction == 0:

                        A = QPointF(coord[2], coord[1])
                        B = QPointF(coord[2] - port.link.width, coord[1] - port.link.length)
                        D = QPointF(coord[2] - port.link.width, coord[1])

                        line = QLineF(D, B)
                        dash_line = self.scene.addLine(line, self.dash_dot_line)
                        dash_line.setZValue(25)
                        self.expanding(port, coord)

                    elif port.direction == 90:

                        A = QPointF(coord[2], coord[3])
                        B = QPointF(coord[2] + port.link.length, coord[3] - port.link.width)
                        D = QPointF(coord[2], coord[3] - port.link.width)

                        line = QLineF(D, B)

                        dash_line = self.scene.addLine(line, self.dash_dot_line)
                        dash_line.setZValue(25)
                        self.expanding(port, coord)


                else:

                    if port.direction == 270:

                        coord[3] += port.link.width

                        A = QPointF(coord[2], coord[3])
                        B = QPointF(coord[2] - port.link.length, coord[3] - port.link.width)
                        D = QPointF(coord[2], coord[3] - port.link.width)

                        line = QLineF(B, D)
                        dash_line = self.scene.addLine(line, self.dash_dot_line)
                        dash_line.setZValue(25)

                    elif port.direction == 180:

                        coord[2] += port.link.width

                        A = QPointF(coord[2], coord[3])
                        B = QPointF(coord[2] - port.link.width, coord[3] + port.link.length)
                        C = QPointF(coord[2] - port.link.width, coord[3] + port.link.length)
                        D = QPointF(coord[2]- port.link.width, coord[3])

                        line = QLineF(D, C)
                        normal_line = self.scene.addLine(line, self.dash_dot_line)
                        normal_line.setZValue(25)


                    elif port.direction == 0:

                        A = QPointF(coord[0], coord[1])
                        B = QPointF(coord[0] + port.link.width, coord[1] - port.link.length)

                        self.expanding(port, coord)

                    elif port.direction == 90:

                        A = QPointF(coord[2], coord[1])
                        B = QPointF(coord[2] + port.link.length, coord[1] + port.link.width)
                        self.expanding(port,coord)

                self.draw_link(port, A, B)


            # draw intersection and normal node

            if Node.type == "intersection":
                A = QPointF(coord[0], coord[1])
                B = QPointF(coord[2], coord[3])
                rect = QRectF(A, B)
                item = self.scene.addRect(rect, self.dot_line, self.brush)
                item.setZValue(25)
                item.setOpacity(0.5)
                item.setToolTip(str(Node.id))

            elif Node.type == "normal":
                A = QPointF(coord[0], coord[1])
                B = QPointF(coord[2], coord[3])

                line = QLineF(A, B)
                dot_line = self.scene.addLine(line, self.dot_line)
                dot_line.setZValue(25)
                dot_line.setToolTip(str(Node.id))


            # print(Node.id, coord, "end")

        else:
            pass
            # print("Node", Node.id,"is already on canvas")

    def draw_link(self, port, A, B):
        # draw link by drawing lanes and merging them.
        if port.link.on_canvas == True:
            return

        x1 = A.x()
        y1 = A.y()

        x2 = B.x()
        y2 = B.y()

        # print('draw',port.link.id , x1,y1,x2,y2)

        # horizontal lanes
        if port.direction == 90:

            interval = (y2 - y1) / port.link.num_lane

            for i in range(port.link.num_lane):
                Lane = port.link.lanes['Lane' + str(port.link.num_lane-i-1)]
                for j in range(port.link.num_sect):
                    if port.type == 'in':
                        cd = Lane['Cell' + str(port.link.num_lane-j-2)]
                        lane = QRectF(QPointF(x2 - cd.offset, y1 + interval * i),
                                      QPointF(x2 - cd.offset - cd.length, y1 + interval * (i + 1)))
                        cd.start_point = [x2,lane.center().y()]
                        port.link.station = [x2,y1, port.direction, port.type]

                    else:
                        cd = Lane['Cell' + str(j)]
                        lane = QRectF(QPointF(x1 + cd.offset, y1 + interval * i),
                                      QPointF(x1 + cd.offset + cd.length, y1 + interval * (i + 1)))
                        cd.start_point = [x1,lane.center().y()]
                        port.link.station = [x1, y2,  port.direction, port.type]

                    lane_item = self.scene.addRect(lane, self.pen, self.brush)
                    lane_item.setZValue(0)
                    lane_item.setOpacity(0.5)
                    lane_item.setToolTip(port.link.id+','+ 'Lane' + str(port.link.num_lane-i-1) +  ','+ cd.id)
                    cd.rect = lane_item


                line = QLineF(QPointF(x1,y1+interval * i),QPointF(x2,  y1 + interval* i ))
                dot_line = self.scene.addLine(line, self.dot_line2)
                dot_line.setZValue(25)


        elif port.direction == 270:

            interval = (y2 - y1) / port.link.num_lane

            for i in range(port.link.num_lane):
                Lane = port.link.lanes['Lane' + str(port.link.num_lane-i-1)]
                for j in range(port.link.num_sect):

                    if port.type == 'in':
                        cd = Lane['Cell' + str(port.link.num_lane-j-2)]
                        lane = QRectF(QPointF(x2+cd.offset, y1 + interval * i), QPointF(x2+cd.offset+cd.length, y1 + interval * (i+1)))
                        port.link.station = [x2, y1,port.direction, port.type]

                    else:
                        cd = Lane['Cell' + str(j)]
                        lane = QRectF(QPointF(x1-cd.offset, y1 + interval * i), QPointF(x1-cd.offset-cd.length, y1 + interval * (i+1)))
                        port.link.station = [x1, y1,  port.direction, port.type]

                    lane_item = self.scene.addRect(lane, self.pen, self.brush)
                    lane_item.setZValue(0)
                    lane_item.setOpacity(0.5)
                    lane_item.setToolTip(port.link.id+','+'Lane' + str(port.link.num_lane-i-1) +','+ cd.id )
                    cd.rect = lane_item

                line = QLineF(QPointF(x1,y1+interval * i),QPointF(x2,  y1 + interval* i ))
                dot_line = self.scene.addLine(line, self.dot_line2)
                dot_line.setZValue(25)

        # vertical lanes
        elif port.direction == 0:

            interval = (x2 - x1) / port.link.num_lane

            for i in range(port.link.num_lane):
                Lane = port.link.lanes['Lane' + str(port.link.num_lane-i-1)]
                for j in range(port.link.num_sect):

                    if port.type == 'in':
                        cd = Lane['Cell' + str(port.link.num_lane-j-2)]
                        lane = QRectF(QPointF(x1+ interval* i,y2 +cd.offset ), QPointF(x1 + interval * (i+1),y2 + cd.offset + cd.length ))
                        port.link.station = [x1, y2, port.direction, port.type]
                    else:
                        cd = Lane['Cell' + str(j)]
                        lane = QRectF(QPointF(x1+ interval* i,y1 -cd.offset ), QPointF(x1 + interval * (i+1),y1 -cd.offset - cd.length ))
                        port.link.station = [x1, y2,  port.direction, port.type]

                    lane_item = self.scene.addRect(lane, self.pen, self.brush)
                    lane_item.setZValue(0)
                    lane_item.setOpacity(0.5)
                    lane_item.setToolTip(port.link.id + ',' + 'Lane' + str(port.link.num_lane-i-1) + ','  + cd.id )
                    cd.rect = lane_item

                line = QLineF(QPointF(x1 +interval * i,y1),QPointF(x1 +interval * i,  y2))
                dot_line = self.scene.addLine(line, self.dot_line2)
                dot_line.setZValue(25)

        elif port.direction == 180:

                interval = (x2 - x1) / port.link.num_lane

                for i in range(port.link.num_lane):
                    Lane = port.link.lanes['Lane' + str(port.link.num_lane-i-1)]
                    for j in range(port.link.num_sect):

                        if port.type == 'in':
                            cd = Lane['Cell' + str(port.link.num_lane - j - 2)]
                            lane = QRectF(QPointF(x1 + interval * i, y2 - cd.offset),
                                          QPointF(x1 + interval * (i + 1), y2 - cd.offset - cd.length))
                            port.link.station = [x1, y2,  port.direction, port.type]
                        else:
                            cd = Lane['Cell' + str(j)]
                            lane = QRectF(QPointF(x1 + interval * i, y1 + cd.offset),
                                          QPointF(x1 + interval * (i + 1), y1 + cd.offset + cd.length))
                            port.link.station = [x1, y1, port.direction, port.type]


                        lane_item = self.scene.addRect(lane, self.pen, self.brush)
                        lane_item.setZValue(0)
                        lane_item.setOpacity(0.5)
                        lane_item.setToolTip(port.link.id + ',' + 'Lane' + str(port.link.num_lane-i-1) + ',' + cd.id)
                        cd.rect = lane_item

                    line = QLineF(QPointF(x1 + interval * i, y1), QPointF(x1 + interval * i, y2))
                    dot_line = self.scene.addLine(line, self.dot_line2)
                    dot_line.setZValue(25)

        port.link.on_canvas = True

    def expanding(self,port,coord):

        # After one node drawing, to draw other connected nodes, we need to adjust draw-starting point.

        if port.direction == 180:
            new_coord = [coord[0], coord[3] + port.link.length, coord[0], coord[3] + port.link.length]

            if port.connected_node.type == "terminal":
                new_coord[0] -= 10
                new_coord[2] += port.connected_node.width + 10
                new_coord[3] += 45

        elif port.direction == 90:
            new_coord = [coord[2] + port.link.length, coord[1], coord[2] + port.link.length, coord[1]]

            if port.connected_node.type == "terminal":
                new_coord[1] -= 10
                new_coord[2] += 45
                new_coord[3] += port.connected_node.height + 10

        elif port.direction == 0:
            new_coord = [coord[0], coord[1] - port.link.length, coord[0], coord[1] - port.link.length]

            if port.connected_node.type == "intersection":
                new_coord[1] -= port.connected_node.height
                new_coord[3] -= port.connected_node.height

            elif port.connected_node.type == "terminal":
                new_coord[0] -= 10
                new_coord[1] -= 45
                new_coord[2] +=  port.connected_node.width +10

        elif port.direction == 270:
            new_coord = [coord[0] - port.link.length, coord[1], coord[0] - port.link.length, coord[1]]

            if port.connected_node.type == "intersection":
                new_coord[0] -= port.connected_node.width
                new_coord[2] -= port.connected_node.width

            elif port.connected_node.type == "terminal":
                new_coord[0] -= 45
                new_coord[1] -= 10
                new_coord[3] += port.connected_node.height + 10

        self.draw_node(port.connected_node, new_coord)



class MyWidget(QWidget):

    def __init__(self, parent):
        # super(FormWidget, self).__init__(parent)
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.view = Map(self)
        self.Net = Network()
        self.timeline = dict()

        # for xml files open
        self.button1 = QPushButton("Button 1")
        self.button1.clicked.connect(lambda:self.file_open())

        self.button2 = QPushButton("Button 2")
        self.button2.clicked.connect(lambda:self.meso_file_open())

        self.gbf = QGroupBox('anime test')
        self.grid = QGridLayout()
        self.gbf.setLayout(self.grid)
        self.text_line = QLineEdit("", self)
        self.grid.addWidget(self.text_line, 0, 0)
        self.button3 = QPushButton("Animation start")
        self.button3.clicked.connect(lambda: self.view.meso_animation(self.timeline))
        self.grid.addWidget(self.button3, 0, 1)

        # just layout for color change test.
        # self.gb = QGroupBox('color test')
        # self.grid = QGridLayout()
        # self.gb.setLayout(self.grid)
        #
        # self.grid.addWidget(QLabel('Link'),0,0)
        # self.combo = QComboBox()
        # self.grid.addWidget(self.combo, 0, 1)
        # for i in range(42):
        #     self.combo.addItem(str(i))
        #
        # self.grid.addWidget(QLabel('Lane'),1,0)
        # self.combo2 = QComboBox()
        # self.grid.addWidget(self.combo2, 1, 1)
        # for i in range(0,3):
        #     self.combo2.addItem(str(i))
        #
        # self.grid.addWidget(QLabel('Cell'),1,2)
        # self.combo3 = QComboBox()
        # self.grid.addWidget(self.combo3, 1, 3)
        # for i in range(0,2):
        #     self.combo3.addItem(str(i))
        #
        # self.grid.addWidget(QLabel('color'), 2, 0)
        # self.combo4 = QComboBox()
        # self.grid.addWidget(self.combo4, 2, 1)
        # self.combo4.addItem('red')
        # self.combo4.addItem('green')
        # self.combo4.addItem('yellow')
        # self.combo4.addItem('None')

        # self.ct_btn = QPushButton('change')
        # self.grid.addWidget(self.ct_btn, 3, 1)
        # self.ct_btn.clicked.connect(lambda:self.color_test(self.combo.currentIndex(),self.combo2.currentIndex(),self.combo3.currentIndex(),self.combo4.currentIndex()))

        self.layout.addWidget(self.view)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.gbf)
        # self.layout.addWidget(self.gb)
        self.setLayout(self.layout)

    def color_test(self,a,b,c,d):
        link = self.Net.Links['Link'+str(a)]
        lane = link.lanes['Lane' + str(b)]
        cell = lane['Cell'+ str(c)]

        if d == 0:
            cell.rect.setBrush(Qt.red)

        elif d == 1:
            cell.rect.setBrush(Qt.green)

        elif d == 2:
            cell.rect.setBrush(Qt.yellow)

        else:
            cell.rect.setBrush(Qt.lightGray)

    def file_open(self):

        #network input open
        ni_file = QFileDialog.getOpenFileName()
        if ni_file[0] == "":
            return

        elif ni_file[0].split(".")[-1] != "xml":
            err = QMessageBox()
            err.about(self, "Load Error", "(only .xmlR file)")
            return

        tree = ET.parse(ni_file[0])
        n_data = tree.getroot()

        set_link_data(self.Net, n_data[2])
        set_node_data(self.Net, n_data[0])
        set_station_data(self.Net,n_data[1])

        #network output open
        no_file = QFileDialog.getOpenFileName()
        if no_file[0] == "":
            return
        elif no_file[0].split(".")[-1] != "xml":
            err = QMessageBox()
            err.about(self, "Load Error", "(only .xmlR file)")
            return

        tree = ET.parse(no_file[0])
        c_data = tree.getroot()
        set_cell_data(self.Net, c_data)

        self.view.draw_network(self.Net)


    def meso_file_open(self):
        #open meso file
        ms_file = QFileDialog.getOpenFileName()
        if ms_file[0] == "":
            return

        elif ms_file[0].split(".")[-1] != "xml":
            err = QMessageBox()
            err.about(self, "Load Error", "(only .xmlR file)")
            return

        tree = ET.parse(ms_file[0])
        ms_data = tree.getroot()
        set_meso_data(ms_data,self.timeline,self.Net)


class Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.form_widget = MyWidget(self)
        # add widget to window
        self.setCentralWidget(self.form_widget)
        self.initUI()

    def initUI(self):

        # status bar
        self.statusBar().showMessage('Ready')

        #some funcs
        exitAction = QAction(QIcon('hmm.png'), 'Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        # menubar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        # toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.resize(1000, 1000)
        self.setWindowTitle('Statusbar')
        # self.setGeometry(300, 300, 300, 200)
        self.center()

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())