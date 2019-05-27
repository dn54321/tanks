from graphics import *
from maps import *
def load_map01(min_width,min_height,width,height,max_width,max_height):
    # Loading Map
        map = Map()
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

        return map

def load_map02(min_width,min_height,width,height,max_width,max_height):
    # Loading Map
        map = Map()
        map.add_spawn([min_width+width*0.1, min_height+height*0.1, 90])
        map.add_spawn([min_width+width*0.9, min_height+height*0.9, 270])

        return map