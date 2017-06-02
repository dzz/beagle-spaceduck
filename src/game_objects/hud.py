from client.beagle.beagle_api import api as bgl
from random import uniform, choice

class hud():
    def __init__(self, player):
        self.player = player
        self.framebuffer = bgl.framebuffer.from_dims(320,120)
        self.filtered_color = [0.0,0.0,0.0]


    def tick(self):   
        def rnd_color():
            return [ uniform(0.0,1.0),uniform(0.0,1.0),uniform(0.0,1.0) ]
        health_str = ""

        rc = rnd_color()
        for i in range(0,3):
            self.filtered_color[i] = self.filtered_color[i]*0.9 + rc[i]*0.1

        filtered_hp_color = []
        filtered_hp_color.extend(self.filtered_color)
        filtered_hp_color[0] = 1.0
        filtered_money_color = []
        filtered_money_color.extend(self.filtered_color)
        filtered_money_color[2] = 1.0


        for health in range(0,int(self.player.health)):
            health_str = health_str + "*"

        money_str = "$:{0}".format(self.player.display_money)
 
        with bgl.context.render_target( self.framebuffer ):
            bgl.context.clear(0.0,0.0,0.0,0.0)
            with bgl.blendmode.alpha_over:
                bgl.lotext.render_text_pixels("HP:{0}".format(health_str), 0,0, filtered_hp_color )
                bgl.lotext.render_text_pixels("HP:{0}".format(health_str), 0,1, [0.2,0.0,1.0] )
                bgl.lotext.render_text_pixels(money_str, 320-(8*len(money_str)),110, filtered_money_color )
                bgl.lotext.render_text_pixels(money_str, 320-(8*len(money_str)),111, [0.5,0.0,1.0] )

    def render(self):
        with bgl.blendmode.alpha_over:
            self.framebuffer.render_processed( bgl.assets.get("beagle-2d/shader/passthru") )

