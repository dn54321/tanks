from graphics import *
from maps import *
from settings import *
from tank import *
import math
from map01 import *
from megarcrazy import *
# MAIN FUNCTION
def start_menu(win,mw,mh,w,h):
    # Inserting Title
    title = Text(Point(mw + 0.5*w, mh + h*0.15), "[Robots]")
    title.setSize(36)
    title.draw(win)
    title.setStyle("bold italic")
    # Lower focused height, (outfocus title)
    mh += h*0.3
    h -= h*0.3

    # Specifying button size and margins
    options=["Select Random Map", "Quit"]
    num_options = len(options)
    gap_size = w * 0.05
    box_height = (h-gap_size*(num_options+1))/num_options
    # Generates buttons
    counter = 1
    button = []
    for name in options:
        rect = Rectangle(Point(w*0.05+mw, mh+counter*(gap_size+box_height)-box_height),
                         Point(w*0.95+mw, mh+counter*(gap_size+box_height)))
        rect.setOutline("black")
        rect.setFill("pink")
        rect.draw(win)
        text = Text(Point(mw+w*0.5, mh+counter*(gap_size+box_height)-box_height/2), 
                    name)
        text.setSize(36)
        text.draw(win)
        button.append([rect, text])
        counter += 1
    q=True
    while(q is True):
        pos = win.getMouse()
        if (pos.getX() > w*0.05+mw and pos.getX() < w*0.95+mw):
            for i in range(num_options):
                if (pos.getY() > mh+(i+1)*(gap_size+box_height)-box_height and pos.getY() < mh+(i+1)*(gap_size+box_height)):
                    if options[i] is "Quit":
                        q = False
                        win.close()
                    elif options[i] is "Select Random Map":
                        q = False
                        for butt in button:
                            butt[0].undraw()
                            butt[1].undraw()
                            title.undraw()

def launch_map(win,minw,minh,w,h,maxw,maxh):
    map = load_map01(minw,minh,w,h,maxw,maxh)
    map.load_map(win)
    tank1 = MC_tank(map.spawn_locations[0], 'blue')
    tank2 = DN_tank(map.spawn_locations[1], 'red')
    tanks = [tank2, tank1]
    for tank in tanks:
        collision = False
        for item in map.objects_points:
            if detect_collision(tank.get_coords(), item,minw,maxw): 
                collision = True
            elif detect_out_of_bounds(tank.get_coords(),minw,minh,maxw,maxh):
                collision = True
        if collision is False:
            tank.draw(win)
    tickUpdate(win,minw,minh,w,h,maxw,maxh,tanks, map)  
        
def tickUpdate(win,minw,minh,w,h,maxw,maxh,tanks, map):
    TANKS.extend(tanks)
    OBJECTS.extend(map.objects_points) 

    time = 0
    while time <= 60*10000000:
        for i in range(SET_TICK):
            if i is 19:
                time += 1
            tanks_to_remove = []
            for tank in tanks:
                tank.shot = False
                tank.action()
                if tank.move == 1:
                    old_x = tank.x
                    old_y = tank.y
                    tank.x = math.sin(tank.dir*math.pi/180)+old_x
                    tank.y = -math.cos(tank.dir*math.pi/180)+old_y
                    collision = False
                    for item in map.objects_points:
                        if detect_collision(tank.get_coords(), item,minw,maxw): 
                            collision = True
                    for other_tank in tanks:
                        if other_tank != tank:
                            if detect_collision(tank.get_coords(), other_tank.get_coords(),minw,maxw): 
                                collision = True
                    if detect_out_of_bounds(tank.get_coords(),minw,minh,maxw,maxh):
                        collision = True
                    if collision is False:
                        tank.draw(win)
                    else:
                        tank.x = old_x
                        tank.y = old_y
                for bullet in tank.bullets:
                    if bullet[2] is 0:
                        bullet[0].draw(win)
                        bullet[2] = 1
                    bullet[0].move(2*math.sin(bullet[1]*math.pi/180), -2*math.cos(bullet[1]*math.pi/180))
                    for coord in bullet[3]:
                        coord[0] += 2*math.sin(bullet[1]*math.pi/180)
                        coord[1] += -2*math.cos(bullet[1]*math.pi/180)
                    collision = False
                    for item in map.objects_points:
                        if detect_collision(bullet[3], item,minw,maxw): 
                            collision = True
                    if detect_out_of_bounds(bullet[3],minw,minh,maxw,maxh):
                        collision = True
                    if collision is True:
                        bullet[0].undraw()
                        tank.bullets.remove(bullet)
                        break
                    if collision is False:
                        for other_tank in tanks:
                            if other_tank is not tank:
                                if detect_collision(bullet[3], other_tank.get_coords(),minw,maxw):
                                    other_tank.obj.undraw()
                                    bullet[0].undraw()
                                    tanks_to_remove.append(other_tank)
                                    tank.bullets.remove(bullet)
            if len(tanks_to_remove) != 0:
                for tank in tanks_to_remove:
                    other_tank.obj.undraw()
                    tanks.remove(tank)
                tanks_to_remove = []
            if len(tanks) is 1:
                print("Winner is {}!".format(tanks[0].color))
                win.close()
                exit(0)
            elif len(tanks) is 0:
                print("It was a tie!")
                exit(0)

        update(SET_TICK)
    win.close()
    print("It was a tie!")

def detect_out_of_bounds(a,minw,minh,maxw,maxh):
    for coord in a:
        if coord[0] <= minw or coord[0] >= maxw or coord[1] <= minh or coord[1] >= maxh:
            return True      
    return False
def detect_collision(list_a,list_b,minw,maxw):
    a = list_a.copy()
    a.append(a[0])
    b = list_b.copy()
    b.append(b[0])
    for coords_A in a:
        prev = None
        num = 0
        if len(b) > 1:
            for coords_B in b:
                if prev == None:
                    prev = coords_B
                else:
                    curr = coords_B
                    if (curr[1] >= coords_A[1] and prev[1] <= coords_A[1]) or (curr[1] <= coords_A[1] and prev[1] >= coords_A[1]):
                        if curr[0] == prev[0]:
                            x = curr[0]
                        elif curr[1] == prev[1]:
                            if (curr[0] >= coords_A[0] and prev[0] <= coords_A[0]) or (curr[0] <= coords_A[0] and prev[0] >= coords_A[0]):
                                return True
                        else:
                            c = curr[1] - (curr[1] - prev[1])/(curr[0]-prev[0])*curr[0]
                            x = (coords_A[1]-c)*(curr[0] - prev[0])/(curr[1]-prev[1])
                        if (coords_A[0] <= x):
                            if ((curr[1] == coords_A[1] and prev[1] != coords_A[1]) or (curr[1] != coords_A[1] and prev[1] == coords_A[1])):
                                break
                            elif (x <= maxw and x >= minw and curr[1] != prev[1]):
                                num += 1
                    prev = coords_B
            if num % 2.0 == 1.0:
                return True
    for coords_B in b:
        if a == [[665.3483495705505, 654.6516504294495], [670.6516504294495, 654.6516504294495], [673.3033008588991, 652.0], [670.6516504294495, 649.3483495705505], [665.3483495705505, 649.3483495705505], [665.3483495705505, 654.6516504294495]] and coords_B == [673.0, 652.0]:
            print("BUG")
        prev = None
        num = 0
        if len(a) > 1:
            for coords_A in a:
                if prev == None:
                    prev = coords_A
                else:
                    curr = coords_A
                    if (curr[1] >= coords_B[1] and prev[1] <= coords_B[1]) or (curr[1] <= coords_B[1] and prev[1] >= coords_B[1]):
                        if curr[0] == prev[0]:
                            x = curr[0]
                        elif curr[1] == prev[1]:
                            if (curr[0] >= coords_B[0] and prev[0] <= coords_B[0]) or (curr[0] <= coords_B[0] and prev[0] >= coords_B[0]):
                                return True
                        else:
                            c = curr[1] - (curr[1] - prev[1])/(curr[0]-prev[0])*curr[0]
                            x = (coords_B[1]-c)*(curr[0] - prev[0])/(curr[1]-prev[1])
                        if (coords_B[0] <= x):
                            if (curr[1] == coords_B[1] and prev[1] != coords_B[1]) or (curr[1] != coords_B[1] and prev[1] == coords_B[1]):
                                num += 0.5
                            elif (x <= maxw and x >= minw and curr[1] != prev[1]):
                                num += 1
                    prev = coords_A
            if num % 2 == 1.0:
                return True 
    return False        

def main(win):
    # Draws border of the program
    win.setBackground("black")
    rect = Rectangle(Point(SET_WIDTH*0.05, SET_HEIGHT*0.05),
                     Point(SET_WIDTH*0.95, SET_HEIGHT*0.95))
    rect.setFill("white")
    rect.draw(win)

    # Creating definitions of the playing field
    min_height = SET_HEIGHT*0.05 
    min_width = SET_WIDTH*0.05
    max_height = SET_HEIGHT*0.95
    max_width = SET_WIDTH*0.95

    height = max_height - min_height
    width = max_width - min_width

    # Show Starting Menu
    start_menu(win,min_width,min_height,width,height)
    # Start The Game!
    launch_map(win, min_width,min_height,width,height,max_height,max_width)

# MAIN FUNCTION CALLER
if __name__ == '__main__':
    #Creates a window and then goes to main function
    win = GraphWin("Tank Challenge", SET_WIDTH, SET_HEIGHT, autoflush=False)
    main(win)
    input("Press anything to exit the program...\n")
    win.close()