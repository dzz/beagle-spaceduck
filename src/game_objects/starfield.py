from random import choice
from random import uniform
from itertools import groupby

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

        self.s *= 0.5 + (1-self.vx)

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
           "rotation_local"       : self.x * -1.1 * self.vx,
           "filter_color"         : self.c,
           "uv_translate"         : [ 0,0 ] }

class starfield(bgl.purging_tick_manager):
    def __init__(self):
        bgl.purging_tick_manager.__init__(self)

    def tick(self):
        bgl.purging_tick_manager.tick(self)
        if( uniform(0.0,1.0) > 0.2 ):
            self.create_tickable( star( s = uniform(0.01,0.3), x = 20, vx = uniform(0.1,0.3), y = uniform( -5, 5) ) )

    def render(self):
        grouped = groupby( self.tickables, lambda x : x.texture )
        for texture, group in grouped:
            for tickable in group:
                star.primitive.render_shaded( star.shader, tickable.get_shader_params() ) 


