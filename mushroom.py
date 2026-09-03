from minescript import player_position, execute, player_inventory_select_slot, player_press_attack, player_press_right, \
    player_press_forward, player_press_left, EventQueue, screen_name
from time import sleep
from threading import Thread
from random import uniform

#variables
starting_cords=[48,67,-46]
ending_cord=[138,67,-46]
next_cords=starting_cords
cords_differences=[[0,0,284],[6,0,0],[0,0,-284],[6,0,0]]
step=0
long_press=(0.5,2)
short_press=(0.1,0.4)


def key_detection(key, action):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while True:
            event = event_queue.get()
            if screen_name() is None and event.action==1:
                if event.key == key:
                    action()

def kill():
    player_press_attack(False)
    player_press_forward(False)
    player_press_right(False)
    player_press_left(False)
    execute(f"\\killjob -1")

def wait_until(statement,interval=0.05):
    while not statement:
        sleep(interval)

Thread(target=key_detection,args=(268,kill)).start()

if [int(x) for x in player_position()]!=starting_cords:
    execute(f"/home")
while True:
    sleep(uniform(*short_press))
    player_inventory_select_slot(0)
    sleep(uniform(*short_press))
    player_press_attack(True)
    while [int(x) for x in player_position()]!=ending_cord:
        match step:
            case 0:
                next_cords+=cords_differences[step]
                step = 1
                player_press_right(True)
                wait_until([int(x) for x in player_position()]==next_cords)
                sleep(uniform(*long_press))
                player_press_right(False)
            case 1:
                next_cords += cords_differences[step]
                step = 2
                player_press_forward(True)
                wait_until([int(x) for x in player_position()]==next_cords)
                sleep(uniform(*short_press))
                player_press_forward(False)
            case 2:
                next_cords += cords_differences[step]
                step = 3
                player_press_left(True)
                wait_until([int(x) for x in player_position()]==next_cords)
                sleep(uniform(*long_press))
                player_press_left(False)
            case 3:
                next_cords += cords_differences[step]
                step = 0
                player_press_forward(True)
                wait_until([int(x) for x in player_position()] == next_cords)
                sleep(uniform(*short_press))
                player_press_forward(False)
    sleep(uniform(*long_press))
    player_press_attack(False)
    sleep(uniform(*long_press))
    execute(f"/home")
