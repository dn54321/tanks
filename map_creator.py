import pickle
from maps import *
from graphics import *

SET_HEIGHT  = 800
SET_WIDTH   = 800

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

    # Loading Map
    map = Map(win)
    p1 = [min_width, min_height]
    p2 = [min_width+width*0.2, min_height]
    p3 = [min_width+width*0.2, min_height + height*0.75]
    p4 = [min_width, min_height + height*0.75]
    object = [p1,p2,p3,p4]
    map.add_object(object)

    p1 = [min_width, max_height]
    p2 = [min_width+width*0.2, max_height]
    p3 = [min_width+width*0.2, max_height-height*0.05]
    p4 = [min_width, max_height-height*0.05]
    object = [p1,p2,p3,p4]
    map.add_object(object)

    p1 = [max_width, max_height]
    p2 = [max_width-width*0.2, max_height]
    p3 = [max_width-width*0.2, max_height-height*0.75]
    p4 = [max_width, max_height-height*0.75]
    object = [p1,p2,p3,p4]
    map.add_object(object)

    p1 = [max_width, min_height]
    p2 = [max_width-width*0.2, min_height]
    p3 = [max_width-width*0.2, min_height+height*0.05]
    p4 = [max_width, min_height+height*0.05]
    object = [p1,p2,p3,p4]
    map.add_object(object)

    p1 = [min_width+width*0.2, min_height]
    p2 = [min_width+width*0.3, min_height]
    p3 = [min_width+width*0.2, min_height+height*0.1]
    object = [p1,p2,p3]
    map.add_object(object)

    p1 = [max_width-width*0.2, max_height]
    p2 = [max_width-width*0.3, max_height]
    p3 = [max_width-width*0.2, max_height-height*0.1]
    object = [p1,p2,p3]
    map.add_object(object)

    map.add_spawn([min_width+width*0.1, min_height+height*0.85, 90])
    map.add_spawn([max_width-width*0.1, max_height-height*0.85, 270])
    map.load_map(win)
# MAIN FUNCTION CALLER
if __name__ == '__main__':
    # Creates a window and then goes to main function
    win = GraphWin("Tank Challenge", SET_WIDTH, SET_HEIGHT, autoflush=False)
    main(win)
    input("Press anything to exit the program...\n")
    win.close()