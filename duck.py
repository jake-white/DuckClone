
class Duck():
    x = 0
    y = 0
    def __init__(self, x, y, velx, vely):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
    def fly(self):
        self.x += self.velx
        self.y += self.vely
    def getX(self):
        return self.x
    def getY(self):
        return self.y