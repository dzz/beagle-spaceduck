from random import uniform, choice
from client.beagle.beagle_api import api as bgl
from .hitbox_effect import hitbox_effect

def rectangles_intersect(a,b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True

class spark():
    decay = 0.9
    lifetime = 50
    primitive = bgl.primitive.unit_uv_square
    shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
    texture = bgl.assets.get("stars/texture/star_2")
    view = bgl.assets.get("beagle-2d/coordsys/16:9")

    def __init__(self,x,y):
        self.t = 0.0
        self.x = x
        self.y = y
        self.vx = uniform(0.1,0.5) * choice([-1,1])
        self.vy = uniform(0.1,0.5) * choice([-1,1])
        self.size = uniform(1.0,2.0)

    def tick(self):
        self.t += 1
        if(self.t>spark.lifetime):
            return False
        self.x += self.vx
        self.y += self.vy
        self.vx = self.vx * spark.decay
        self.vy = self.vy * spark.decay
        return True

    def get_shader_params(self):
        return { 
            "texBuffer"            : spark.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.2 + self.vx * self.size,0.2 + self.vy*self.size ],
            "translation_world"    : [ self.x, self.y],
            "scale_world"          : [ 1, 1],
            "view"                 : spark.view,
            "rotation_local"       : self.size * self.vx * self.y,
            "filter_color"         : [ 1.0,0.5,0.2,0.1 ],
            "uv_translate"         : [ 0,0 ] }


class collisions(bgl.purging_tick_manager):

    player_bullet_height = 0.1
    base_enemy_size = 0.31

    def __init__(self, **kwargs):
        bgl.purging_tick_manager.__init__(self)
        self.player = kwargs['player']
        self.enemies = kwargs['enemies']
        self.enemy_bullets = kwargs['enemy_bullets']
        self.sparks = []
        self.hitbox_effect = self.create_tickable( hitbox_effect() )
        
    def tick(self):
        bgl.purging_tick_manager.tick(self)
        for s in self.sparks:
            if not s.tick(): 
                self.sparks.remove(s)

        self.sparks = self.sparks[-64:]
        for player_bullet in self.player.player_bullets.tickables:
            for enemy in self.enemies.enemies.tickables:
                enemy_size = collisions.base_enemy_size * enemy.size
                a = [ player_bullet.x-player_bullet.vx, player_bullet.y - collisions.player_bullet_height, 
                      player_bullet.x+player_bullet.vx, player_bullet.y + collisions.player_bullet_height ]
                b = [ enemy.x - enemy_size, enemy.y - enemy_size, 
                      enemy.x + enemy_size, enemy.y + enemy_size ]
                if( rectangles_intersect( a,b ) ):
                    enemy.register_hit()
                    self.hitbox_effect.add_hitbox(a)
                    self.hitbox_effect.add_hitbox(b)
                    for x in range( 0, 4 ):
                        self.sparks.append(spark( enemy.x, enemy.y))
        for enemy_bullet in self.enemy_bullets.tickables:
                bullet_size = 0.04
                player_size = 0.23
                a = [ self.player.x - player_size, self.player.y - player_size,
                      self.player.x + player_size, self.player.y + player_size ]
                b = [ enemy_bullet.x - bullet_size, enemy_bullet.y - bullet_size, 
                      enemy_bullet.x + bullet_size, enemy_bullet.y + bullet_size ]
                if( rectangles_intersect( a,b ) ):
                    self.player.register_hit()
                    self.hitbox_effect.add_hitbox(a)
                    self.hitbox_effect.add_hitbox(b)
                    self.enemy_bullets.tickables.remove(enemy_bullet)
                        

    def render(self):
        for renderable in self.sparks:
            spark.primitive.render_shaded( spark.shader, renderable.get_shader_params() ) 
        self.hitbox_effect.render()


