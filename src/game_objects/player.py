from client.beagle.beagle_api import api as bgl

class player(bgl.simple_tick_manager):
    def __init__(self, **kwargs):
        bgl.simple_tick_manager.__init__(self)
        self.primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
        self.view = bgl.assets.get("beagle-2d/coordsys/16:9")
        self.sequencer = self.create_tickable( bgl.assets.get("spaceduck-sprite/curve_sequence/spaceduck_mouth_closed") )

        self.x = 0.0
        self.y = 0.0


    def tick(self):
        bgl.simple_tick_manager.tick(self)
        diff_x = self.x + bgl.gamepads.find_primary().left_stick[0]*0.7;
        diff_y = self.y + bgl.gamepads.find_primary().left_stick[1]*0.7;

        self.x = (self.x * 0.8) + (diff_x*0.2)
        self.y = (self.y * 0.8) + (diff_y*0.2)

        if(self.x < -7): 
            self.x = -7
        if(self.x > 7 ):
            self.x =7
        if(self.y < -4):
            self.y = -4
        if(self.y > 4 ):
            self.y =4

       
    def get_shader_params(self):
        return {
            "texBuffer"            : bgl.assets.get( self.sequencer.animated_value("texture_name") ),
            "translation_local"    : [ self.x, self.y ],
            "scale_local"          : [ 1.0,1.0],
            "translation_world"    : [ 0, 0],
            "scale_world"          : [ 1, 1],
            "view"                 : self.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }

    def render(self):
        self.primitive.render_shaded( self.shader, self.get_shader_params() )
