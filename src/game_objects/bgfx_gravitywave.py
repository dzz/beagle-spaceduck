from client.beagle.beagle_api import api as bgl

class bgfx_gravitywave():
    speed = 0.01

    def __init__(self, **kwargs):
        self.primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("bgfx-shaders/shader/bgfx_gravitywave")
        self.background_texture = bgl.assets.get("bgfx-shaders/texture/space_background_0")
        self.gradient_texture = bgl.assets.get("bgfx-shaders/texture/space_gradient_0")
        self.overlay_texture = bgl.assets.get("bgfx-shaders/texture/space_overlay_0")
        self.t = 0.0
        self.player = kwargs["player"]

    def tick(self):
        self.t += bgfx_gravitywave.speed
            

    def get_shader_params(self):
        return {
            "time" : self.t,
            "player_y" : self.player.y,
            "player_x" : self.player.x * 0.2,
            "background" : self.background_texture,
            "gradient" : self.gradient_texture,
            "overlay" : self.overlay_texture
        }

    def render (self):
        self.primitive.render_shaded( self.shader, self.get_shader_params() )
