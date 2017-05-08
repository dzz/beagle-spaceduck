from client.beagle.beagle_api import api as bgl

class bgfx_gravitywave():
    speed = 0.02

    def __init__(self):
        self.primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("bgfx-shaders/shader/bgfx_gravitywave")
        self.gradient_texture = bgl.assets.get("bgfx-shaders/texture/space_gradient_0")
        self.overlay_texture = bgl.assets.get("bgfx-shaders/texture/space_overlay_0")
        self.t = 0.0

    def tick(self):
        self.t += bgfx_gravitywave.speed
            

    def get_shader_params(self):
        return {
            "time" : self.t,
            "gradient" : self.gradient_texture,
            "overlay" : self.overlay_texture
        }

    def render (self):
        self.primitive.render_shaded( self.shader, self.get_shader_params() )
