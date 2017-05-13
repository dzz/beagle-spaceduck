from math import sin
from client.beagle.beagle_api import api as bgl

class basic_enemy():
    view = bgl.assets.get("beagle-2d/coordsys/16:9")
    texture = bgl.assets.get("bullets/texture/basic_bullet")

    def __init__(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']

        self.halo_amt = 0.0

    def tick(self):
        self.x -= 0.1
        if(self.x > -20):
            return True

    def get_shader_params(self ):
        return { 
            "texBuffer"            : basic_enemy.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.1,0.1],
            "translation_world"    : [ self.x, self.y],
            "scale_world"          : [ 1, 1],
            "view"                 : basic_enemy.view,
            "rotation_local"       : self.x * 0.8,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }


class pulse_emitter():
    def __init__(self, **kwargs):
        self.t = 0
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.rate = kwargs['rate']
        self.range = kwargs['range']
        self.ramp_speed = kwargs['ramp_speed']
        self.template = kwargs['template']
        self.ramp = 0.0
        

    def emit(self):
        self.template(self)

    def tick(self):
        self.t = self.t + self.rate
        if(self.t > self.range[1]):
            return False
        if(self.t > self.range[0]):
           self.ramp = self.ramp + self.ramp_speed
           if self.ramp > 1.0:
                self.ramp = 0.0
                self.emit()

        return True

  
class enemies(bgl.simple_tick_manager):
    primitive = bgl.primitive.unit_uv_square 
    shader = bgl.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self):
        bgl.purging_tick_manager.__init__(self)
      
        self.enemies = self.create_tickable( bgl.purging_tick_manager() )
        self.emitters = self.create_tickable( bgl.purging_tick_manager() )

        self.create_emitter ( pulse_emitter( x = 20, y = 0, 
                                      rate = 1.0/60.0, 
                                      range =(5.0,15), 
                                      ramp_speed = 0.05, 
                                      template = (lambda emitter : self.create_enemy(emitter) ) ))

    def create_emitter(self, emitter ):
        return self.emitters.create_tickable( emitter )

    def create_enemy( self, emitter ):
        return self.enemies.create_tickable( basic_enemy( x = emitter.x, y = emitter.y ) )

    def render( self ):
        for enemy in self.enemies.tickables:
            enemies.primitive.render_shaded( enemies.shader, enemy.get_shader_params() )

