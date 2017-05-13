from math import sin
from client.beagle.beagle_api import api as bgl
from .pulse_emitter import pulse_emitter

class basic_enemy():
    view = bgl.assets.get("beagle-2d/coordsys/16:9")
    texture = bgl.assets.get("bullets/texture/basic_bullet")
    driver_rate = 1.0 / 60.0

    def __init__(self, **kwargs):
        self.x = self.base_x = kwargs['x']
        self.y = self.base_y = kwargs['y']
        self.driver = bgl.curve_driver( curve = bgl.assets.get("enemy_paths/curve/" + kwargs["sequence_key"] ),
                                          rate = basic_enemy.driver_rate )

    def tick(self):
        self.driver.tick()
        if(self.driver.is_finished()):
            return False

        p = self.driver.value()
        self.x = self.base_x + p[0]
        self.y = self.base_y + p[1]

        return True

    def get_shader_params(self ):
        return { 
            "texBuffer"            : basic_enemy.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.25,0.25],
            "translation_world"    : [ self.x, self.y],
            "scale_world"          : [ 1, 1],
            "view"                 : basic_enemy.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }



  
class enemies(bgl.simple_tick_manager):
    primitive = bgl.primitive.unit_uv_square 
    shader = bgl.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self):
        bgl.purging_tick_manager.__init__(self)
      
        self.enemies = self.create_tickable( bgl.purging_tick_manager() )
        self.emitters = self.create_tickable( bgl.purging_tick_manager() )

        self.create_emitter ( pulse_emitter( x = 0, y = 0, 
                                      rate = 1.0/60.0, 
                                      start = 0.0,
                                      ramp_speed = 0.05, 
                                      sequence_key = "up_down",
                                      template = (lambda emitter : self.create_enemy(emitter, "slow_move_left") ) ))

    def create_emitter(self, emitter ):
        return self.emitters.create_tickable( emitter )

    def create_enemy( self, emitter, sequence_key ):
        return self.enemies.create_tickable( basic_enemy( x = emitter.x, y = emitter.y, sequence_key = sequence_key ) )

    def render( self ):
        for enemy in self.enemies.tickables:
            enemies.primitive.render_shaded( enemies.shader, enemy.get_shader_params() )

