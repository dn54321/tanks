from settings import *
import math
from abc import ABC, abstractmethod
from tank import Tank

#####################################################################
#  [SUMMARY OF COMMANDS]
#  Full description:
#  self.set_angle(degree) | sets the angle of the tank to degree in True bearing notation 0 -> N,90 -> E, etc..
#  self.degree get_angle()| returns angle of tank
#  self.shoot()           | shoots bullet
#  self.search()          | returns a dictionary that holds { 
#                                                             x: posx of the location | note does not represent center of object
#                                                             y: posy of the location |
#                                                             #type: "WALL" or "BULLET" or "TANK"
#                                                             distance: float (how far it is from center of tank)
#                                                            }
# [size of stuff] (not to scale)                                                    (0, self.radius/4)
# Tank @ 45 deg:            . (0,self.radius)               Bullet @ 45 degrees     .     . (self.radius/4,self.radius/4)
#                                                                             
#   (-self.radius,0)  .     X     . (self.radius,0)       (-self.radius/4,0)  .     X     . (self.radius/4,0)
#
#                           . (0,-self.radius)                                      . (0,-self.radius/4)
#
# where x is the center of your object (used to track position) currently at (0,0)
class MC_tank(Tank):
    def __init__(self, spawn_loc, color='black'):
        super().__init__(spawn_loc, color)
        # VARIABLES THAT PERSIST OVER MULTIPLE CALLS
    def action(self):
        self.set_angle(30)
        self.move_tank(1)
class DN_tank(Tank):
    def __init__(self, spawn_loc, color='black'):
        super().__init__(spawn_loc, color)
        # VARIABLES THAT PERSIST OVER MULTIPLE CALLS
    def action(self):
        self.set_angle(90)
        self.move_tank(1)
