def rectangles_intersect(a,b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True

class collisions():
        player_bullet_height = 0.01
        enemy_size = 0.1

    def __init__(self, **kwargs):
        self.player = kwargs['player']
        self.player_bullets = kwargs['player_bullets']
        self.enemies = kwargs['enemies']
        self.enemy_bullets = kwargs['enemy_bullets']
        
    def tick(self):
        for player_bullet in self.player_bullets.tickables:
            for enemy in self.enemies:
                a = [ player_bullet.x, player_bullet.y - collisions.player_bullet_height, 
                      player_bullet.x +player_bullet.v_x, player_bullet.y + collisions.player_bullet_height ]
                b = [ enemy.x - collisions.enemy_size, enemy.y - collisions.enemy_size, 
                      enemy.x + collisions.enemy_size, enemy.y + collisions.enemy_size ]
                if( rectangles_intersect( a,b ) ):
                    enemy.register_hit()

