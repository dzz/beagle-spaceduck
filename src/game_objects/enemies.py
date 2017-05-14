from math import sin
from client.beagle.beagle_api import api as bgl
from .pulse_emitter import pulse_emitter
from .motion_modulators import motion_modulators
from .bullet_patterns import bullet_patterns

class enemy(bgl.simple_tick_manager):
    view = bgl.assets.get("beagle-2d/coordsys/16:9")
    texture = bgl.assets.get("bullets/texture/basic_bullet")
    driver_rate = 1.0 / 60.0

    def __init__(self, **kwargs):

        bgl.simple_tick_manager.__init__(self) 
        self.enemy_bullets = kwargs['enemy_bullets']
        self.x = self.base_x = kwargs['emitter'].x
        self.y = self.base_y = kwargs['emitter'].y
        self.driver = self.create_tickable( bgl.curve_driver( curve = bgl.assets.get("enemy_paths/curve/" + kwargs["driver"] ),
                                          rate = enemy.driver_rate ))


        modulator_def = kwargs['modulator']
        self.bullet_color = kwargs['bullet_color']
        self.modulator_args = [self]
        self.modulator_args.extend(modulator_def[1])

        self.modulator = motion_modulators[modulator_def[0]]

        bullet_pattern_params = kwargs['bullet_pattern']['params']
        bullet_pattern_params['enemy'] = self

        self.bullet_pattern = self.create_tickable( bullet_patterns[kwargs['bullet_pattern']['type']]( **bullet_pattern_params ) )
        
    def tick(self):
        bgl.simple_tick_manager.tick(self)
        if(self.driver.is_finished()):
            return False

        p = self.driver.value()
        self.x = self.base_x + p[0]
        self.y = self.base_y + p[1]

        self.modulator(*self.modulator_args)
        return True

    def get_shader_params(self ):
        return { 
            "texBuffer"            : enemy.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ 0.25,0.25],
            "translation_world"    : [ self.x, self.y],
            "scale_world"          : [ 1, 1],
            "view"                 : enemy.view,
            "rotation_local"       : 0.0,
            "filter_color"         : [ 1.0, 1.0, 1.0, 1.0],
            "uv_translate"         : [ 0,0 ] }



class enemies(bgl.simple_tick_manager):
    primitive = bgl.primitive.unit_uv_square 
    shader = bgl.assets.get("beagle-2d/shader/beagle-2d")

    def __init__(self, **kwargs):
        bgl.purging_tick_manager.__init__(self)
      
        self.enemies = self.create_tickable( bgl.purging_tick_manager() )
        self.emitters = self.create_tickable( bgl.purging_tick_manager() )
        self.enemy_bullets = kwargs['enemy_bullets']

        self.load_stage()

    def create_emitter(self, emitter ):
        return self.emitters.create_tickable( emitter )

    def create_enemy( self, **kwargs ):
        return self.enemies.create_tickable( enemy( **kwargs ) )

    def load_stage(self):
        def parse_enemy_to_args(emitter, key):
            enemy_def = bgl.assets.get("enemy_defs/enemy/"+key)

            return {
                "emitter": emitter,
                "enemy_bullets" : self.enemy_bullets,
                "driver": enemy_def["driver"],
                "modulator" : enemy_def["modulator"],
                "bullet_pattern" : enemy_def["bullet_pattern"],
                "bullet_color" : enemy_def["bullet_color"]
            } 

        emitter_defs = bgl.assets.get( "test_stage/emitter_script/test_script")["emitters"]
        for emitter_def in emitter_defs:
            self.create_emitter(
                pulse_emitter (
                    rate = 1.0 / 60.0,
                    start = emitter_def["t"],
                    x = emitter_def["location"][0],
                    y = emitter_def["location"][1],
                    ramp_speed = emitter_def["speed"],
                    driver = emitter_def["driver"],
                    template = (lambda emitter: self.create_enemy(**parse_enemy_to_args( emitter, emitter_def["enemy"] )))
                    )
                )

    def render( self ):
        for enemy in self.enemies.tickables:
            enemies.primitive.render_shaded( enemies.shader, enemy.get_shader_params() )

