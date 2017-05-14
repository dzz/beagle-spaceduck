class steady_fire_left():
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


bullet_patterns = {
    "steady_fire_left" : steady_fire_left
}
