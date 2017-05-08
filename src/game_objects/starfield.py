from random import choice
from random import uniform

from client.beagle.beagle_api import api as bgl

class star():
    view = bgl.assets.get("beagle-2d/coordsys/16:9")
    shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
    primitive = bgl.primitive.unit_uv_square
    textures = [
                    bgl.assets.get("stars/texture/star_0"),
                    bgl.assets.get("stars/texture/star_1"),
                    bgl.assets.get("stars/texture/star_2"),
                    bgl.assets.get("stars/texture/star_3")
               ]
    colors = [
            [ 0.5,0.5,0.5,1.0 ],
            [ 0.7,0.5,0.9,1.0 ],
            [ 0.3,0.3,0.3,1.0 ],
            [ 1.0,1.0,1.0,1.0 ],
    ]

    def __init__(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.vx = kwargs['vx']
        self.s = kwargs['s']
        self.c = list(map( lambda x : x * self.s, choice( star.colors) ))
        self.texture = choice( star.textures )

    def tick(self):
        self.x -= self.vx 
        return (self.x > -10)

    def get_shader_params(self):
       return {
           "texBuffer"            : self.texture,
           "translation_local"    : [ 0, 0 ],
           "scale_local"          : [ self.s, self.s ],
           "translation_world"    : [ self.x, self.y],
           "scale_world"          : [ 1, 1],
           "view"                 : star.view,
           "rotation_local"       : self.x * -0.1 * self.vx,
           "filter_color"         : self.c,
           "uv_translate"         : [ 0,0 ] }

class starfield(bgl.purging_tick_manager):
    def __init__(self):
        bgl.purging_tick_manager.__init__(self)

    def tick(self):
        bgl.purging_tick_manager.tick(self)
        if( uniform(0.0,1.0) > 0.7 ):
            self.create_tickable( star( s = uniform(0.01,0.8), x = 20, vx = uniform(0.1,0.9), y = uniform( -5, 5) ) )

    def render(self):
        for tickable in self.tickables:
            star.primitive.render_shaded( star.shader, tickable.get_shader_params() ) 


