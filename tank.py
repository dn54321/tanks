import math
from graphics import *
from settings import *
from abc import ABC, abstractmethod
class Tank(ABC):
    def __init__(self, spawn_loc, color='black'):
        self.x = spawn_loc[0]
        self.y = spawn_loc[1]
        self.dir = spawn_loc[2]
        self.radius = 15
        self.move = 0
        self.color = color
        self.ammo = 3
        self.recharge = SET_TICK * 5
        self.bullets = []
        self.shot = False
        self.obj = None
    # Turns the tank to a certain position.
    def set_angle(self, angle):
        self.dir = angle
    
    # gets the angle
    def get_angle(self):
        return self.dir

    # If 1, the tank moves forward every tick.
    # If 0, the tank does not move.
    def move_tank(self, num):
        self.move = num

    # Can shoot up to three bullets
    # Upon exhausting bullets, you have to wait 5sec
    # Only one bullet can be shot per tick
    def shoot(self):
        if self.ammo is not 0 and self.shot is False:
            self.ammo -= 1
            #bullet = Point(self.x,self.y)
            bullet_point = [self.transform([0,-self.radius/4]),
                            self.transform([self.radius/4,0]),
                            self.transform([self.radius/4,self.radius/4]),
                            self.transform([0,self.radius/4]),
                            self.transform([-self.radius/4,0])]
            point_list = []
            for points in bullet_point:
                point_list.append(Point(points[0],points[1]))
            bullet = Polygon(point_list)
            self.bullets.append([bullet,self.dir,0,bullet_point])
            bullet.setFill(self.color)
        self.shot = True

    def draw(self, win):
        list = []
        if self.obj is not None:
            self.obj.undraw()
        for points in self.get_coords():
            list.append(Point(points[0],points[1]))
        obj_shape = Polygon(list)
        obj_shape.setFill(self.color)
        obj_shape.setOutline(self.color)
        obj_shape.draw(win)
        self.obj = obj_shape 

    def get_coords(self):
        p = [[0,self.radius],[self.radius,0],[0,-self.radius],[-self.radius,0]]
        return [self.transform(p[0]),self.transform(p[1]),self.transform(p[2]),self.transform(p[3])]

    def transform(self, p):
        x = math.cos(math.radians(45-self.dir))*p[0]-math.sin(math.radians(45-self.dir))*p[1]+self.x
        y = -math.sin(math.radians(45-self.dir))*p[0]-math.cos(math.radians(45-self.dir))*p[1]+self.y
        return [x,y]

    @abstractmethod
    def action(self):
        if self.ammo is 0:
            self.recharge -= 1
        if self.recharge is 0:
            self.ammo = 3
            self.recharge = SET_TICK * 5
        if self.color == 'blue':
       #     self.set_angle(0)
       #     a = self.search()
            self.set_angle(30)
            a = self.search()
            print("{},{},{},{}".format(a.x,a.y,a.type,a.distance))
            self.set_angle(0)
            a = self.search()
            print("{},{},{},{}".format(a.x,a.y,a.type,a.distance))
           # if len(self.bullets) == 0:
           #     self.shoot()
        if self.color == 'red':
            self.set_angle(-45)
           # if len(self.bullets) == 0:
            #    self.shoot()

    def search(self):
        opponent_bullets = []
        opponent_tanks = []
        for tank in TANKS:
            if tank != self:
                opponent_tanks.append(tank.get_coords())
                for bullet in tank.bullets:
                    opponent_bullets.append(bullet[3])
        minh = SET_HEIGHT*0.05 
        minw = SET_WIDTH*0.05
        maxh = SET_HEIGHT*0.95
        maxw = SET_WIDTH*0.95
        return self.find_shortest(OBJECTS, opponent_tanks, opponent_bullets, minw,maxw,minh,maxh)

    def find_shortest(self, walls, tanks, bullets, minw,maxw,minh,maxh):
        # Notes to consider
        # angle at 180 degrees
        tank_angle = self.dir % 360
        if self.dir%180 != 0:
            y_c = 1                                 # y cofficient
            x_c = math.tan(math.radians(90-self.dir))   # x cofficient
            if x_c == -0.9999999999999999:
                x_c = -1
            elif x_c == 0.9999999999999999:
                x_c = 1
            c = self.y + x_c*self.x                 # line constant
        else:
            c = self.x
            y_c = 0
            x_c = 1


        # What if object has 1 point?
  #      if len(walls) == 1:
  #          if (y_c*walls[0][1] + x_c*walls[0][0] == c and eq_degree(tank_angle,[x_c,y_c],[walls[0][0],walls[0][1]])):
  #              return Block(walls[0][0],walls[0][1],"wall",find_distance([self.x,self.y],[walls[0][0],walls[0][1]]))
  #      if len(tanks) == 1:
  #          if (y_c*tanks[0][1] + x_c*tanks[0][0] == c and eq_degree(tank_angle,[x_c,y_c],[tanks[0][0],tanks[0][1]])):
  #              return Block(tanks[0][0],tanks[0][1],"tank",find_distance([self.x,self.y],[tanks[0][0],tanks[0][1]]))
  #      if len(bullets) == 1:
  #          if (y_c*bullets[0][1] + x_c*bullets[0][0] == c and eq_degree(tank_angle,[x_c,y_c],[bullets[0][0],bullets[0][1]])):
  #              return Block(bullets[0][0],bullets[0][1],"bullet",find_distance([self.x,self.y],[bullets[0][0],bullets[0][1]]))

        # What if object has 2 points?
        distance = -1
        obj_type="wall"
        wall_dist = get_shortest([x_c,y_c,c,self.x,self.y], walls, tank_angle)
        tank_dist = get_shortest([x_c,y_c,c,self.x,self.y], tanks, tank_angle)
        bullet_dist = get_shortest([x_c,y_c,c,self.x,self.y], bullets, tank_angle)
        if wall_dist[2] != -1:
            if distance == -1:
                distance = wall_dist[2]
                obj_type = "wall"
                x = wall_dist[0]
                y = wall_dist[1]
        if tank_dist[2] != -1:
            if distance == -1:
                distance = tank_dist[2]
                obj_type = "tank"
                x = tank_dist[0]
                y = tank_dist[1]                     
            elif tank_dist[2] < distance:
                distance = tank_dist[2]
                obj_type = "tank"
                x = tank_dist[0]
                y = tank_dist[1]
        if bullet_dist[2] != -1:
            if distance == -1:
                distance = bullet_dist[2]
                obj_type = "bullet"    
                x = bullet_dist[0]
                y = bullet_dist[1]                 
            elif bullet_dist[2] < distance:
                distance = bullet_dist[2]
                obj_type = "bullet"
                x = bullet_dist[0]
                y = bullet_dist[1]

        # NO OBSTACLE FOUNDS -> Level Boundary
        if distance < 0:
            # 0 or 180 degrees
            if tank_angle == 0:
                return Block(self.x,minh,"wall",self.y-minh)
            elif tank_angle == 180:
                return Block(self.x,maxh,"wall",maxh-self.y)
            # 90 or 270 degrees
            elif tank_angle == 90:
                return Block(maxw,self.y,"wall",maxw-self.x)
            elif tank_angle == 270:
                return Block(minw,self.y,"wall",self.x-minw)
            # every other degree
            for x in [minw, maxw]:
                y = x_c*x + c
                if (y >= minh and y <= maxh):
                    return Block(x,y,"wall",find_distance([self.x,self.y],[x,y]))
            for y in [minh, maxh]:
                x = (y-c)/x_c
                if (x >= minw and x <= maxw):
                    return Block(x,y,"wall",find_distance([self.x,self.y],[x,y]))
        return Block(x,y,obj_type,distance)

def get_shortest(line, objects, dir):
    # line [x_c,y_c,c,x,y]
    # output: [x,y,dist]
    # Closest distance item
    shortest_distance = -1
    short_x = short_y = None
    p1 = None
    if len(objects) == 0:
        return [short_x,short_y,-1]
    for object in objects:
        object_dup = object.copy()
        object_dup.append(object[0])
        p1 = p2 = None
        for point in object_dup:
            if p1 is None:
                p1 = point
            else:
                p2 = point

                # Line Properties of Object
                y_c = p2[0]-p1[0]                  # y cofficient

                x_c = p1[1]-p2[1]                  # x cofficient
                c = y_c*p1[1] + x_c*p1[0]          # line constant

                # Matrix Solution
                determinant = (line[0]*y_c - line[1]*x_c)
                if (determinant <= -0.000001 or determinant >= 0.000001): # Contains intersection
                    x = (y_c*line[2] - line[1]*c)/determinant
                    y = (line[0]*c - x_c*line[2])/determinant
                    if x <= max(p1[0],p2[0]) and x >= min(p1[0],p2[0]) and y <= max(p1[1],p2[1]) and y >= min(p1[1],p2[1]):
                        if eq_degree(dir, [line[3],line[4]], [x,y]):
                            obj_distance = find_distance([line[3],line[4]],[x,y])
                            if (obj_distance < shortest_distance or shortest_distance == -1):
                                shortest_distance = obj_distance
                                short_x = x 
                                short_y = y
                p1 = point
    return [short_x,short_y,shortest_distance]

def find_distance(p1,p2):
    # c^2 = a^2 + b^2
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def eq_degree(dir, p1, p2):
    if (p1[0] == p2[0]):
        if (p2[1] <= p1[1] and dir == 0): # y inverted
            return True
        elif (p2[1] >= p1[1] and dir == 180):
            return True
    else:
        angle = math.degrees(math.atan2((p2[1]-p1[1]),(p2[0]-p1[0])))
        debug = (90+angle)%360
        if (math.fabs(dir-debug) < 1):
            return True
    return False    

# Valid Types: BULLET, WALL, TANK, POINT (not used)
class Block:
    def __init__(self, x,y,type,distance = -1):
        self.x = x
        self.y = y
        self.distance = distance
        self.type = type.upper()

