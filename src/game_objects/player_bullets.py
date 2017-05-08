from math import sin
from client.beagle.beagle_api import api as bgl

class basic_bullet():
    view = bgl.assets.get("beagle-2d/coordsys/16:9")
    texture = bgl.assets.get("bullets/texture/basic_bullet")

    def __init__(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.vx = kwargs['vx']

    def tick(self):
        self.x += self.vx
        self.vx *= 1.1
        self.y = self.y + (0.02 * sin(self.x*2))
        if(self.x > 10):
            return False
        return True

    def get_shader_params(self, effects_buffer):
        if effects_buffer:
            return {
                "texBuffer"            : basic_bullet.texture,
                "translation_local"    : [ 0, 0 ],
                "scale_local"          : [ 0.3,0.4],
                "translation_world"    : [ self.x, self.y],
                "scale_world"          : [ 1, 1],
                "view"                 : basic_bullet.view,
                "rotation_local"       : self.x * -3,
                "filter_color"         : [ 0.4, 0.2, 1.0, 1.0],
                "uv_translate"         : [ 0,0 ] }
        else:
            return { 
                "texBuffer"            : basic_bullet.texture,
                "translation_local"    : [ 0, 0 ],
                "scale_local"          : [ 0.2,0.2],
                "translation_world"    : [ self.x, self.y],
                "scale_world"          : [ 1, 1],
                "view"                 : basic_bullet.view,
                "rotation_local"       : self.x * 4,
                "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
                "uv_translate"         : [ 0,0 ] }


class player_bullets(bgl.purging_tick_manager):
    def __init__(self, **kwargs):

        bgl.purging_tick_manager.__init__(self)

        self.bullet_primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
        self.cooldown = 0.0
        self.player = kwargs['player']
        self.view = bgl.assets.get("beagle-2d/coordsys/16:9")

    def tick(self):
        bgl.purging_tick_manager.tick(self)

        if(self.player.firing):
            self.fire()

        self.cooldown -= 0.1

    def fire(self):
        if(self.cooldown < 0.0):
            self.create_bullet()
            self.cooldown = 0.4

    def create_bullet(self):
        self.create_tickable( basic_bullet( x = self.player.x + 0.2, y = self.player.y, vx = 0.15 ) )

    def render(self, **kwargs ):
        for bullet in self.tickables:
            self.bullet_primitive.render_shaded( self.shader, bullet.get_shader_params( kwargs['effects_buffer'] ) )


