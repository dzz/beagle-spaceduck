from client.beagle.beagle_api import api as bgl

from .game_objects.player import player
from .game_objects.bgfx_gravitywave import bgfx_gravitywave

class game(bgl.simple_tick_manager):

    def init(self):
        self.player = self.create_tickable( player() )
        self.bgfx_gravitywave = self.create_tickable( bgfx_gravitywave() )

    def render(self):
        self.bgfx_gravitywave.render()

        with bgl.blendmode.alpha_over:
            self.player.render()

    def finalize(self):
        pass

    def configure(self, application_ini):
        pass
