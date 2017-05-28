from client.beagle.beagle_api import api as bgl
from random import choice

class hitbox_effect(bgl.basic_sprite_renderer):
    shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
    def __init__(self):
        self.hitboxes = [] 
        self.texture = bgl.texture.from_data(1,1,[1.0,1.0,1.0,1.0])
        self.state = True
        
    def add_hitboxes(self, hitboxes):
        self.hitboxes.extend(hitboxes)
        self.state = not self.state

    def tick(self):
        pass

    def get_params(self,hitbox):

        center_x = hitbox[0]
        center_y = hitbox[1]

        scale_x = hitbox[2]-hitbox[0]
        scale_y = hitbox[3]-hitbox[1]

        view = bgl.assets.get("beagle-2d/coordsys/16:9")

        if self.state:
            color = [1.0,1.0,1.0,1.0]
        else:
            color = choice( [[1.0,1.0,0.0,1.0], [0.0,1.0,1.0,1.0], [1.0,0.0,1.0,1.0]])

        return { 
            "texBuffer"            : self.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ scale_x, scale_y ],
            "translation_world"    : [ center_x, center_y ],
            "scale_world"          : [ 1, 1],
            "view"                 : view,
            "rotation_local"       : 0.0,
            "filter_color"         : color, 
            "uv_translate"         : [ 0,0 ] }
       

    def render(self):
        for h in self.hitboxes:
            bgl.primitive.unit_uv_square.render_shaded(hitbox_effect.shader, self.get_params(h))
            self.state = not self.state
        self.hitboxes = []
