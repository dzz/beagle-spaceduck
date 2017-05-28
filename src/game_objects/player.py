from client.beagle.beagle_api import api as bgl
from .player_bullets import player_bullets

class player(bgl.simple_tick_manager):
    def __init__(self, **kwargs):
        bgl.simple_tick_manager.__init__(self)
        self.primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
        self.view = bgl.assets.get("beagle-2d/coordsys/16:9")
        self.idle_sequencer = self.create_tickable( bgl.assets.get("spaceduck-sprite/curve_sequence/spaceduck_mouth_closed") )
        self.firing_sequencer = self.create_tickable( bgl.assets.get("spaceduck-sprite/curve_sequence/spaceduck_mouth_open") )
        self.player_bullets = self.create_tickable( player_bullets( player = self ) )

        self.x = 0.0
        self.y = 0.0

        self.firing = False

    def tick(self):
        self.gamepad = bgl.gamepads.find_primary()
        bgl.simple_tick_manager.tick(self)
        diff_x = self.x + self.gamepad.left_stick[0]*0.9;
        diff_y = self.y + self.gamepad.left_stick[1]*0.9;

        if(self.gamepad.button_down( bgl.gamepads.buttons.A )):
                self.firing = True
        else:
                self.firing = False


        self.x = (self.x * 0.9) + (diff_x*0.1)
        self.y = (self.y * 0.9) + (diff_y*0.1)

        if(self.x < -7.2): 
            self.x = -7.2
        if(self.x > 7.2 ):
            self.x =7.2
        if(self.y < -4):
            self.y = -4
        if(self.y > 4 ):
            self.y =4

       
    def register_hit(self):
        pass

    def get_shader_params(self):

        if self.firing:
            sequencer = self.firing_sequencer
        else:
            sequencer = self.idle_sequencer

        return {
            "texBuffer"            : bgl.assets.get( sequencer.animated_value("texture_name") ),
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.8, 0.6 ],
            "translation_world"    : [ self.x, self.y],
            "scale_world"          : [ 1.0,1.0 ],
            "view"                 : self.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }

    def render(self):
        self.primitive.render_shaded( self.shader, self.get_shader_params() )
