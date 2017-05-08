from client.beagle.beagle_api import api as bgl

class basic_bullet():
    view = bgl.assets.get("beagle-2d/coordsys/16:9")

    def __init__(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.vx = kwargs['vx']

    def tick(self):
        self.x += self.vx
        if(self.x > 10):
            return False
        return True

    def get_shader_params(self):
        return {
            "texBuffer"            : bgl.assets.get( "spaceduck-sprite/texture/spaceduck_mouth_open_0" ),
            "translation_local"    : [ self.x, self.y ],
            "scale_local"          : [ 0.75,0.75],
            "translation_world"    : [ 0, 0],
            "scale_world"          : [ 1, 1],
            "view"                 : basic_bullet.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }


class player_bullets(bgl.purging_tick_manager):
    def __init__(self, **kwargs):

        bgl.purging_tick_manager.__init__(self)

        self.bullet_primitive = bgl.primitive.unit_uv_square
        self.shader = bgl.assets.get("beagle-2d/shader/beagle-2d")
        self.cooldown = 0.0
        self.player = kwargs['player']
        self.view = bgl.assets.get("beagle-2d/coordsys/16:9")

    def tick(self):
        bgl.purging_tick_manager.tick(self)

        if(self.player.firing):
            self.fire()

        self.cooldown -= 0.1

    def fire(self):
        if(self.cooldown < 0.0):
            self.create_bullet()
            self.cooldown = 1.0

    def create_bullet(self):
        self.create_tickable( basic_bullet( x = self.player.x, y = self.player.y, vx = 0.1 ) )

    def render(self):
        for bullet in self.tickables:
            self.bullet_primitive.render_shaded( self.shader, bullet.get_shader_params() )


