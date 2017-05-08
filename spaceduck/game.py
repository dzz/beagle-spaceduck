from client.beagle.beagle_api import api as bgl

from .game_objects.player import player

class game(bgl.simple_tick_manager):

    def init(self):
        self.player = self.create_tickable( player() )

    def render(self):
        self.player.render()

    def finalize(self):
        pass

    def configure(self, application_ini):
        pass
