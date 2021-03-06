from random import choice, uniform
from client.beagle.beagle_api import api as bgl
from math import sin, cos, floor
from itertools import chain

class explosions(bgl.basic_sprite_renderer):
    textures = None
    num_textures = 16
    primitive = bgl.primitive.unit_uv_square 
    shader = bgl.assets.get("beagle-2d/shader/beagle-2d")

    def generate_texture():
        size = choice( [ 32,64,128,256 ] )
        num_parts = int(uniform(8.0,size))
        colors = [ [1.0,0.0,1.0,1.0],
                    [0.5,0.0,1.0,1.0],[1.0,1.0,1.0,1.0] ]
        image = []
        for i in range(0, size*size):
            image.append([0.0,0.0,0.0,0.0])

        for i in range(0, num_parts):
            r = uniform(0.0,3.14*2)
            d = uniform(0.0,0.7)
            x,y = cos(r)*d, sin(r)*d
            x,y = x +1, y+ 1
            x,y = x * size, y * size
            x,y = floor(x / 2.0), floor(y / 2.0)

            image[ int( (y*size)+x) ] = choice( colors )

        return bgl.texture.from_data(size,size,list(chain(*image)))

    def add_explosion(self, dead_item):
        dead_item.explosion_life = 1.0
        self.dead_items.append( dead_item )
        self.explosion_impulse = 1.0
        dead_item.texture = choice( explosions.textures )

    def render(self):
        for renderable in self.dead_items:
            dead_item = renderable
            sparams = renderable.get_shader_params()
            el = dead_item.explosion_life
            sparams["filter_color"] = [ el,el,el,el*0.5]
            sparams["rotation_local"] = 0.0
            explosions.primitive.render_shaded( explosions.shader, sparams )
            renderable.size = renderable.size * 1.1
            
    def generate_textures():
        explosions.textures = []
        for i in range( 0, explosions.num_textures ):
            explosions.textures.append( explosions.generate_texture() )

    def tick(self):
        self.explosion_impulse = self.explosion_impulse * 0.98
        for dead_item in self.dead_items:
            dead_item.explosion_life = dead_item.explosion_life *0.9
            dead_item.tick()
            if dead_item.explosion_life < 0.1:
                self.dead_items.remove(dead_item)
        return True

    def __init__(self):
        self.explosion_impulse = 1.0
        self.dead_items = []
        if not explosions.textures:
            explosions.generate_textures()
