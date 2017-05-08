from client.beagle.beagle_api import api as bgl

class bgfx_gravitywave():
    speed = 0.01

    def __init__(self):
        self.primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("bgfx-shaders/shader/bgfx_gravitywave")
        self.t = 0.0

    def tick(self):
        self.t += bgfx_gravitywave.speed
            

    def get_shader_params(self):
        return {
            "time" : self.t
        }

    def render (self):
        self.primitive.render_shaded( self.shader, self.get_shader_params() )
