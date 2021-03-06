from client.beagle.beagle_api import api as bgl

from .game_objects.player import player
from .game_objects.bgfx_gravitywave import bgfx_gravitywave
from .game_objects.starfield import starfield
from .game_objects.enemies import enemies
from .game_objects.enemy_bullets import enemy_bullets
from .game_objects.collisions import collisions

from .gfx_util.uniform_fade import uniform_fade
from .editor import editor

class game(bgl.simple_tick_manager, bgl.basic_web_app):

    passthru_shader = bgl.assets.get("beagle-2d/shader/passthru")
    postfx_shader = bgl.assets.get("filters/shader/postfx_filter")

    def init(self):
        self.editor = editor
        self.player = self.create_tickable( player() )
        self.enemy_bullets = self.create_tickable( enemy_bullets() )
        self.enemies = self.create_tickable( enemies( enemy_bullets = self.enemy_bullets ) )
        self.last_frame = bgl.framebuffer.from_screen()
        self.current_frame = bgl.framebuffer.from_screen()
        self.blur_effects_buffer = bgl.framebuffer.from_screen()
        self.bgfx_gravitywave = self.create_tickable( bgfx_gravitywave( player = self.player, distortion_buffer = self.blur_effects_buffer.get_texture()) )
        self.starfield = self.create_tickable( starfield() )
        self.collisions = self.create_tickable( collisions( player = self.player, enemies = self.enemies, enemy_bullets = self.enemy_bullets ))

    def render(self):
        with bgl.context.render_target( self.last_frame):
            self.current_frame.render_processed( game.passthru_shader )

        with bgl.context.render_target( self.blur_effects_buffer):
                with bgl.blendmode.alpha_over:
                    uniform_fade.apply_fadeout(0.9 - (0.85*self.collisions.explosions.explosion_impulse))
                with bgl.blendmode.add:
                    #self.starfield.render()
                    self.collisions.render()
                with bgl.blendmode.alpha_over:
                    self.player.player_bullets.render( effects_buffer = True )
                    self.enemy_bullets.render( effects_buffer = True )

        with bgl.context.render_target( self.current_frame):
            with bgl.blendmode.alpha_over:
                self.last_frame.render_processed( game.passthru_shader )
                self.bgfx_gravitywave.render()
                with bgl.blendmode.add:
                    self.starfield.render()
                    self.blur_effects_buffer.render_processed( game.passthru_shader )
                self.enemies.render()
                self.player.render()
                with bgl.blendmode.add:
                    #self.collisions.render()
                    self.enemy_bullets.render()
                self.player.player_bullets.render( effects_buffer = False )
                self.player.hud.render()

        self.current_frame.render_processed( game.postfx_shader, { "excitement" : [ self.collisions.explosions.explosion_impulse ], "pain" : [self.player.injury_impulse ]} )

    def finalize(self):
        pass

    def configure(self, application_ini):
        pass

    def get_version_info(self):
        return {
            "application" : "SPACE DUCK SUPREME",
            "version" : "1.0"
        }
