from client.beagle.beagle_api import api as bgl

from .game_objects.player import player
from .game_objects.bgfx_gravitywave import bgfx_gravitywave

class game(bgl.simple_tick_manager):

    def init(self):
        self.player = self.create_tickable( player() )
        self.bgfx_gravitywave = self.create_tickable( bgfx_gravitywave() )
        self.last_frame = bgl.framebuffer.from_screen()
        self.current_frame = bgl.framebuffer.from_screen()

    def render(self):
        self.bgfx_gravitywave.render()

        with bgl.context.render_target( self.last_frame):
            self.current_frame.render_processed( bgl.assets.get("beagle-2d/shader/passthru") )

        with bgl.context.render_target( self.current_frame):
            with bgl.blendmode.alpha_over:
                self.last_frame.render_processed( bgl.assets.get("beagle-2d/shader/passthru") )
                self.bgfx_gravitywave.render()
                self.player.render()

        self.current_frame.render_processed( bgl.assets.get("beagle-2d/shader/passthru") )

    def finalize(self):
        pass

    def configure(self, application_ini):
        pass
