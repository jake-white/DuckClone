import time


class GameTimer(object):
    shouldBeRunning = False
    lastTimeTicked = 0

    def __init__(self, tick, interval = 10):
        self.tick = tick
        self.interval = interval

    def start(self):
        self.shouldBeRunning = True
        print("Game loop starting...")
        while self.shouldBeRunning:
            if(time.time() * 1000 - self.lastTimeTicked >= self.interval):
                self.lastTimeTicked = time.time() * 1000
                self.tick()

    def stop(self):
        self.shouldBeRunning = False