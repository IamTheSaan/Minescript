from minescript import player_position, EventQueue, queue, echo, entities, player_press_use, player_hand_items, player_inventory_select_slot
from time import sleep
from random import uniform
from utils.timer import FpsTimer

# ==================================
#          CONFIGURATION
# ==================================
reaction_time=(0.2,0.4)
CATCH = {"!!!"}
recast_time=7
anti_recast=3
Fps = 50
# ==================================

def r_btn():
    player_press_use(True)
    player_press_use(False)

timer = FpsTimer(Fps)
start_x, start_y, start_z = player_position()
last_catch=0
anti_recast_counter=0
with EventQueue() as event_queue:
    event_queue.register_key_listener()
    running = True
    while running:
        timer.tick()
        last_catch += 1

        if anti_recast_counter > 0:
            anti_recast_counter-=1
            continue

        curr_x, curr_y, curr_z = player_position()
        delta_cords = abs(start_x - curr_x), abs(start_y - curr_y), abs(start_z - curr_z)
        if any(x>1 for x in delta_cords):
            echo("Player has been moved")
            running=False
            continue

        if player_hand_items().main_hand['item'] == "minecraft:fishing_rod":
            pass
        else:
            echo("No fishing rod")
            running = False
            continue

        if last_catch >= recast_time * Fps:
            echo("Hook got stuck on something, recasting.")
            player_inventory_select_slot(1)
            sleep(uniform(*reaction_time))
            player_inventory_select_slot(0)
            last_catch = 0
            sleep(uniform(*reaction_time))
            r_btn()

        if any(e.name in CATCH for e in entities()):
            sleep(uniform(*reaction_time))
            r_btn()
            sleep(uniform(*reaction_time))
            r_btn()
            last_catch = 0
            anti_recast_counter = anti_recast

        try:
            while event := event_queue.get(False):
                if event.key == 268 and event.action == 1:
                    running = False
                    echo("Home key pressed")
        except queue.Empty:
            pass