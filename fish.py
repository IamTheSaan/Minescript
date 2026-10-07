from minescript import player_position, execute, player_inventory_select_slot, player_press_attack, player_press_right, \
    player_press_forward, player_press_left, EventQueue, screen_name, queue, echo, entities, player_press_use, player_hand_items
from time import sleep
from random import uniform
from utils.timer import FpsTimer
reaction_time=(0.2,0.4)
def RBtn():
    player_press_use(True)
    player_press_use(False)



CATCH = {"!!!"}
timer = FpsTimer(100)
with EventQueue() as event_queue:
    event_queue.register_key_listener()
    running = True
    while running:
        timer.tick()

        if player_hand_items.name == "minecraft:fishing_rod":
            pass
        else:
            running = False

        if any(e.name in CATCH for e in entities()):
            sleep(uniform(*reaction_time))
            RBtn()
            sleep(uniform(*reaction_time))
            RBtn()


        try:
            while event := event_queue.get(False):
                if event.key == 268 and event.action == 1:
                    running = False
                    echo("Home key pressed")
        except queue.Empty:
            pass