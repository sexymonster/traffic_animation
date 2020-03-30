# traffic_animation

btn1 calls two file open dialogs.

First, choose Network input file and Network output file in sequence.
Map will be drawn.

After that, click btn2 to open the meso file.

At last, click the animation start button and you can see the animation.

class Map(QGraphicsView) is scene of map
and class MyWidget(QWidget) is whole widgets including map, btns.
