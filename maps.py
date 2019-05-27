from graphics import *

class Map():
    def __init__(self, size=None):
        self.player_size = size
        self.objects_points = []
        self.objects = []
        self.spawn_locations = []

    def add_object(self, obj):
        self.objects_points.append(obj)

    def add_spawn(self, point):
        self.spawn_locations.append(point)

    def add_win(self, win):
        self.win = win

    def load_map(self, win):
        for obj in self.objects_points:
            list = []
            for points in obj:
                list.append(Point(points[0],points[1]))
            obj_shape = Polygon(list)
            obj_shape.setFill("black")
            obj_shape.setOutline("black")
            obj_shape.draw(win)
            self.objects.append(obj_shape)
  #      for obj in self.spawn_locations:
  #         Point(obj[0],obj[1]).draw(win)
  #          d = Point(700,100)
  #          d.setFill('blue')
  #          d.draw(win)
    def clear_map(self, win):
        for obj in self.objects:
            obj.undraw(self.win)
            self.objects.remove(obj)
