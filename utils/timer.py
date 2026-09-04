from time import sleep, time

class FpsTimer:
    def __init__(self, fps:int):
        self.delay = 1/fps
        self.last_activated = 0

    def tick(self):
        to_wait = self.last_activated + self.delay - time()
        if to_wait > 0:
            sleep(to_wait)
        self.last_activated = time()