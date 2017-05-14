from math import sin,cos

class steady_fire_horizontal():
    def __init__(self, **kwargs ):
        self.t = 0
        self.enemy = kwargs['enemy']
        self.idle_frames = kwargs['idle_frames']
        self.vx = kwargs['vx']

    def tick(self):
        self.t += 1 
        if(self.t > self.idle_frames):
            self.t = 0
            self.enemy.enemy_bullets.create_bullet( x = self.enemy.x, y = self.enemy.y, vx = self.vx, vy = 0.0, color = self.enemy.bullet_color )

class arc():
    def __init__(self, **kwargs ):
        self.t = 0.0
        self.arc_t = 0.0
        self.enemy = kwargs['enemy']
        self.idle_frames = kwargs['idle_frames']
        self.speed = kwargs['speed']
        self.v = kwargs['v']

    def tick(self):
        self.t += 1.0 
        self.arc_t += 1.0
        if(self.t > self.idle_frames):
            self.t = 0.0
            vx = sin(self.arc_t * self.speed ) * self.v
            vy = cos(self.arc_t * self.speed ) * self.v
            
            self.enemy.enemy_bullets.create_bullet( x = self.enemy.x, y = self.enemy.y, vx = vx, vy = vy, color = self.enemy.bullet_color )



bullet_patterns = {
    "steady_fire_horizontal" : steady_fire_horizontal,
    "arc" : arc
}
