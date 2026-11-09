from minescript import player_position, execute, player_inventory_select_slot, player_press_attack, player_press_right, \
    player_press_forward, player_press_left, EventQueue,  queue, echo, entities, player_press_use, player_orientation
from time import sleep
from random import uniform
from utils.timer import FpsTimer
from utils.directions import Directions
from utils.rotation import look_at
#---------------------------------------
#            CONFIGURATION
#---------------------------------------
long_reaction_time=(0.5,1.3)
vacuum_hold=(0.8,1.1)
reaction_time=(0.2,0.4)
#=======================================



#=======================================
#              COORDINATES
#=======================================
starting_waypoint=[48,67,49]
ending_waypoint=[138,67,49]
cords_differences=[[0,0,189],[6,0,0],[0,0,-189],[6,0,0]]

step=0
waypoints=[[48,67,49],[48, 67, 238], [54, 67, 238], [54, 67, 49], [60, 67, 49], [60, 67, 238], [66, 67, 238], [66, 67, 49], [72, 67, 49], [72, 67, 238], [78, 67, 238], [78, 67, 49], [84, 67, 49], [84, 67, 238], [90, 67, 238], [90, 67, 49], [96, 67, 49], [96, 67, 238], [102, 67, 238], [102, 67, 49], [108, 67, 49], [108, 67, 238], [114, 67, 238], [114, 67, 49], [120, 67, 49], [120, 67, 238], [126, 67, 238], [126, 67, 49], [132, 67, 49], [132, 67, 238], [138, 67, 238], [138, 67, 49]]
last_cords=starting_waypoint


#=======WAYPOINT CALCULATION=======
#
# def add_vector(a,b):
#     return [x+y for x,y in zip(a,b)]
#
# def fill_way(start,stop,cord_diff,waypoints):
#     step=0
#     next_cord=start
#     waypoints+=start
#     while next_cord!=stop:
#         next_cord=add_vector(next_cord,cord_diff[step%4])
#         waypoints.append(next_cord)
#         step+=1
# fill_way(starting_waypoint,ending_waypoint,cords_differences,waypoints)
# print(waypoints)
#
#===================================

def in_area(cords, start, end):
    if  (start[0]<=cords[0]<=end[0] or start[0]>=cords[0]>=end[0]) and (start[1]<=cords[1]<=end[1] or start[1]>=cords[1]>=end[1]) and (start[2]<=cords[2]<=end[2] or start[2]>=cords[2]>=end[2]):
        return True
    return False

def which_way(start,end):
    if start[0]==end[0] and (start[0]-48)%12==0:
        return Directions.RIGHT
    if start[0]==end[0] and (start[0]-54)%12==0:
        return Directions.LEFT
    if start[2]==end[2]:
        return Directions.FORWARD
    return False

def stop_moving():
    player_press_forward(False)
    player_press_right(False)
    player_press_left(False)

def distance(a,b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

PESTS={"Silverfish","Bat"}
def pest():
    if any(e.name in PESTS for e in entities(max_distance=11)):
        stop_moving()
        sleep(uniform(*reaction_time))
        player_press_attack(False)
        sleep(uniform(*reaction_time))
        player_inventory_select_slot(2)
        sleep(uniform(*reaction_time))
        while all_entities:=[e for e in entities(max_distance=14) if e.name in PESTS]:
            vacuum(all_entities[0].position)
        player_inventory_select_slot(1)
        while distance(player_orientation(),(-90,3))>0.1:
            player_press_attack(True)
            player_press_attack(False)
            sleep(uniform(0.1,0.15))
        player_inventory_select_slot(0)
        player_press_attack(True)
        sleep(uniform(*reaction_time))
        return True
    return False

def vacuum(cords):
    look_at(*cords)
    sleep(uniform(*reaction_time))
    player_press_use(True)
    sleep(uniform(*vacuum_hold))
    player_press_use(False)
    sleep(uniform(*reaction_time))

def looping():
    global step
    step = 0
    sleep(uniform(*long_reaction_time))
    player_press_attack(False)
    stop_moving()
    sleep(uniform(*long_reaction_time))
    execute("home")
    sleep(uniform(*reaction_time))
    player_press_attack(True)
    player_press_right(True)
    sleep(uniform(0.8, 1.2))
    player_press_right(False)

timer = FpsTimer(100)
counter=0
with EventQueue() as event_queue:
    event_queue.register_key_listener()
    running = True
    if [int(x) for x in player_position()] != starting_waypoint:
        execute("home")
    sleep(uniform(*reaction_time))
    player_inventory_select_slot(0)
    sleep(uniform(*reaction_time))
    player_press_attack(True)
    while running:
        timer.tick()
        curr_cords = [int(x) for x in player_position()]

        if not in_area(curr_cords,waypoints[step],waypoints[step+1]):
            counter+=1
            if counter>=100:
                running = False
                echo("exited area")
                continue
        else:
            counter=0

        if pest():
            continue

        if curr_cords==ending_waypoint:
            looping()
            continue

        if curr_cords==waypoints[step+1]:
            step+=1
            if which_way(waypoints[step],waypoints[step+1])==Directions.LEFT or which_way(waypoints[step],waypoints[step+1])==Directions.RIGHT:
                sleep(uniform(*reaction_time))
                stop_moving()
            elif which_way(waypoints[step],waypoints[step+1])==Directions.FORWARD:
                sleep(uniform(*long_reaction_time))

        direction = which_way(waypoints[step],waypoints[step+1])
        match direction:
            case Directions.RIGHT:
                if in_area(curr_cords,waypoints[step],waypoints[step+1]):
                    player_press_right(True)
            case Directions.LEFT:
                if in_area(curr_cords,waypoints[step],waypoints[step+1]):
                    player_press_left(True)
            case Directions.FORWARD:
                if in_area(curr_cords,waypoints[step],waypoints[step+1]):
                    player_press_forward(True)
        try:
            while event := event_queue.get(False):
                if event.key == 268 and event.action == 1:
                    running = False
                    echo("Home key pressed")
        except queue.Empty:
            pass

    stop_moving()
    player_press_attack(False)