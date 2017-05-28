from client.beagle.beagle_api import api as bgl

class enemy_bullet():
    view = bgl.assets.get("beagle-2d/coordsys/16:9")
    texture = bgl.assets.get("bullets/texture/basic_bullet")

    def __init__(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.vx = kwargs['vx']
        self.vy = kwargs['vy']
        self.color = kwargs['color']
    
    def tick(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

        if( self.x < -20 ):
            return False
        if( self.x > 20 ):
            return False
        if( self.y < -10 ):
            return False
        if( self.y > 10 ):
            return False
 
        return True

    def get_shader_params(self):
        return { 
            "texBuffer"            : enemy_bullet.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.2,0.2],
            "translation_world"    : [ self.x, self.y],
            "scale_world"          : [ 1, 1],
            "view"                 : enemy_bullet.view,
            "rotation_local"       : self.x * 0.8,
            "filter_color"         : self.color,
            "uv_translate"         : [ 0,0 ] }

class enemy_bullets(bgl.purging_tick_manager):
        def __init__(self):
            bgl.purging_tick_manager.__init__(self)
            self.bullet_primitive = bgl.primitive.unit_uv_square
            self.shader = bgl.assets.get("beagle-2d/shader/beagle-2d")

        def create_bullet(self, **kwargs):
            self.create_tickable(enemy_bullet(**kwargs))

        def render(self, effects_buffer = False ):
            for bullet in self.tickables:
                self.bullet_primitive.render_shaded(self.shader, bullet.get_shader_params() )
        

