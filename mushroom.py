from minescript import player_position, execute, player_inventory_select_slot, player_press_attack, player_press_right, \
    player_press_forward, player_press_left, EventQueue, screen_name, queue, echo
from time import sleep,time
from random import uniform
from utils.timer import FpsTimer
from utils.directions import Directions
#variables
starting_waypoint=[48,-61,-46]
ending_waypoint=[138,-61,-46]
last_cords=starting_waypoint
cords_differences=[[0,0,284],[6,0,0],[0,0,-284],[6,0,0]]
long_press=(0.5,3)
short_press=(0.1,0.4)
step=0
waypoints=[[48, -61, -46], [48, -61, 238], [54, -61, 238], [54, -61, -46], [60, -61, -46], [60, -61, 238], [66, -61, 238], [66, -61, -46], [72, -61, -46], [72, -61, 238], [78, -61, 238], [78, -61, -46], [84, -61, -46], [84, -61, 238], [90, -61, 238], [90, -61, -46], [96, -61, -46], [96, -61, 238], [102, -61, 238], [102, -61, -46], [108, -61, -46], [108, -61, 238], [114, -61, 238], [114, -61, -46], [120, -61, -46], [120, -61, 238], [126, -61, 238], [126, -61, -46], [132, -61, -46], [132, -61, 238], [138, -61, 238], [138, -61, -46], [138, -61, -46]]


def add_vector(a,b):
    return [x+y for x,y in zip(a,b)]

def fill_way(start,stop,cord_diff,waypoints):
    step=0
    next_cord=start
    while next_cord!=stop:
        next_cord=add_vector(next_cord,cord_diff[step%4])
        waypoints.append(next_cord)
        step+=1
    waypoints.append(stop)

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

def key_detection(key, action):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while True:
            event = event_queue.get()
            if screen_name() is None and event.action==1:
                if event.key == key:
                    action()

def stop_moving():
    player_press_forward(False)
    player_press_right(False)
    player_press_left(False)

def wait_until(statement,interval=0.05):
    print(statement)
    while not statement():
        sleep(interval)


"""
if [int(x) for x in player_position()]!=starting_cords:
    execute(f"/home")
while True:
    sleep(uniform(*short_press))
    player_inventory_select_slot(0)
    sleep(uniform(*short_press))
   # player_press_attack(True)
    while [int(x) for x in player_position()]!=ending_cord:
        match step:
            case 0:
                next_cords=add_vector(next_cords,cords_differences[step])
                step = 1
                print(next_cords)
                player_press_right(True)
                wait_until(lambda : [int(x) for x in player_position()]==next_cords)
                sleep(uniform(*long_press))
                player_press_right(False)
            case 1:
                next_cords=add_vector(next_cords,cords_differences[step])
                step = 2
                player_press_forward(True)
                wait_until(lambda : [int(x) for x in player_position()]==next_cords)
                sleep(uniform(*short_press))
                player_press_forward(False)
            case 2:
                next_cords=add_vector(next_cords,cords_differences[step])
                step = 3
                player_press_left(True)
                wait_until(lambda : [int(x) for x in player_position()]==next_cords)
                sleep(uniform(*long_press))
                player_press_left(False)
            case 3:
                next_cords=add_vector(next_cords,cords_differences[step])
                step = 0
                player_press_forward(True)
                wait_until(lambda : [int(x) for x in player_position()] == next_cords)
                sleep(uniform(*short_press))
                player_press_forward(False)
    sleep(uniform(*long_press))
    player_press_attack(False)
    sleep(uniform(*long_press))
    execute(f"/home")
"""
timer = FpsTimer(100)
with EventQueue() as event_queue:
    event_queue.register_key_listener()
    running = True
    if [int(x) for x in player_position()] != starting_waypoint:
        execute("home")
    sleep(uniform(*short_press))
    player_inventory_select_slot(0)
    sleep(uniform(*short_press))
    while running:
        timer.tick()
        curr_cords = [int(x) for x in player_position()]

        if curr_cords==ending_waypoint:
            step=0
            sleep(uniform(*long_press))
            player_press_attack(False)
            sleep(uniform(*long_press))
            execute("home")
            sleep(uniform(*short_press))
            player_press_attack(True)
            continue


        if curr_cords==waypoints[step+1]:
            step+=1
            if which_way(waypoints[step],waypoints[step+1])==Directions.LEFT or which_way(waypoints[step],waypoints[step+1])==Directions.RIGHT:
                sleep(uniform(*short_press))
                stop_moving()
            elif which_way(waypoints[step],waypoints[step+1])==Directions.FORWARD:
                sleep(uniform(*long_press))

        if not in_area(curr_cords,waypoints[step],waypoints[step+1]):
            running = False
            echo("exited area")
            continue

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