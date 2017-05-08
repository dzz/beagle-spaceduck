from client.beagle.beagle_api import api as bgl

class player(bgl.simple_tick_manager):
    def __init__(self):
        bgl.simple_tick_manager.__init__(self)
        self.primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
        self.view = bgl.assets.get("beagle-2d/coordsys/16:9")
        self.sequencer = self.create_tickable( bgl.assets.get("spaceduck-sprite/curve_sequence/spaceduck_mouth_closed") )

    def get_shader_params(self):
        return {
            "texBuffer"            : bgl.assets.get( self.sequencer.animated_value("texture_name") ),
            "translation_local"    : [ 0.0,0.0],
            "scale_local"          : [ 1.0,1.0],
            "translation_world"    : [ 0, 0],
            "scale_world"          : [ 1, 1],
            "view"                 : self.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }

    def render(self):
        self.primitive.render_shaded( self.shader, self.get_shader_params() )
