from client.beagle.beagle_api import api as bgl

from .game_objects.player import player
from .game_objects.bgfx_gravitywave import bgfx_gravitywave

class game(bgl.simple_tick_manager):

    passthru_shader = bgl.assets.get("beagle-2d/shader/passthru")

    def init(self):
        self.player = self.create_tickable( player() )
        self.bgfx_gravitywave = self.create_tickable( bgfx_gravitywave( player = self.player ) )
        self.last_frame = bgl.framebuffer.from_screen()
        self.current_frame = bgl.framebuffer.from_screen()
        self.bullets_buffer = bgl.framebuffer.from_dims(64,64, filtered = True )

    def render(self):
        self.bgfx_gravitywave.render()

        with bgl.context.render_target( self.last_frame):
            self.current_frame.render_processed( game.passthru_shader )

        with bgl.context.render_target( self.bullets_buffer):
                bgl.context.clear( 0.0, 0.0, 0.0, 0.0)
                self.player.player_bullets.render( effects_buffer = True )

        with bgl.context.render_target( self.current_frame):
            with bgl.blendmode.alpha_over:
                self.last_frame.render_processed( game.passthru_shader )
                self.bgfx_gravitywave.render()
                self.player.player_bullets.render( effects_buffer = False )
                with bgl.blendmode.add:
                    self.bullets_buffer.render_processed( game.passthru_shader )
                self.player.render()



        self.current_frame.render_processed( game.passthru_shader )

    def finalize(self):
        pass

    def configure(self, application_ini):
        pass
