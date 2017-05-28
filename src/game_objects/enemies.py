from math import sin
from client.beagle.beagle_api import api as bgl
from .pulse_emitter import pulse_emitter
from .motion_modulators import motion_modulators
from .bullet_patterns import bullet_patterns

class enemy(bgl.simple_tick_manager):
    view = bgl.assets.get("beagle-2d/coordsys/16:9")
    driver_rate = 1.0 / 60.0

    def __init__(self, **kwargs):

        bgl.simple_tick_manager.__init__(self) 
        self.enemy_bullets = kwargs['enemy_bullets']
        self.x = self.base_x = kwargs['emitter'].x
        self.y = self.base_y = kwargs['emitter'].y
        self.driver = self.create_tickable( bgl.curve_driver( curve = bgl.assets.get("enemy_paths/curve/" + kwargs["driver"] ),
                                          rate = enemy.driver_rate ))


        self.size = kwargs['size']
        self.texture = bgl.assets.get("enemy-sprites/texture/" + kwargs['sprite'])
        modulator_def = kwargs['modulator']
        self.bullet_color = kwargs['bullet_color']
        self.modulator_args = [self]
        self.modulator_args.extend(modulator_def[1])

        self.modulator = motion_modulators[modulator_def[0]]

        bullet_pattern_params = kwargs['bullet_pattern']['params']
        bullet_pattern_params['enemy'] = self

        self.bullet_pattern = self.create_tickable( bullet_patterns[kwargs['bullet_pattern']['type']]( **bullet_pattern_params ) )
        self.hp = kwargs['hp']
        self.size = kwargs['size']
        self.rot = 0.0
        self.tick() #prime render
        
    def register_hit(self, explosions):
        self.hp = self.hp - 1
        self.rot += 0.1
        if(self.hp <= 0.0):
            self.tickables.remove(self.bullet_pattern)
            explosions.add_explosion( self )

    def tick(self):
        self.rot *=0.9
        if( self.hp <= 0):
            return False
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
            "texBuffer"            : self.texture,
            "translation_local"    : [ 0, 0 ],
            "scale_local"          : [ self.size,self.size],
            "translation_world"    : [ self.x, self.y],
            "scale_world"          : [ 1, 1],
            "view"                 : enemy.view,
            "rotation_local"       : self.rot,
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

    def create_enemy( self, emitter, **kwargs ):
        kwargs["emitter"] = emitter
        return self.enemies.create_tickable( enemy( **kwargs ) )

    def load_stage(self):
        def parse_enemy_to_args(key):
            enemy_def = bgl.assets.get("enemy_defs/enemy/"+key)

            defargs = { "enemy_bullets" : self.enemy_bullets }

            for key in enemy_def:
                defargs[key] = enemy_def[key]

            return defargs 
            #return {
            #    "enemy_bullets" : self.enemy_bullets,
            #    "driver": enemy_def["driver"],
            #    "modulator" : enemy_def["modulator"],
            #    "bullet_pattern" : enemy_def["bullet_pattern"],
            #    "bullet_color" : enemy_def["bullet_color"],
            #    "sprite" : enemy_def["sprite"]
            #} 

        emitter_defs = bgl.assets.get( "test_stage/emitter_script/test_script")["emitters"]
        for emitter_def in emitter_defs:
            factory_args = parse_enemy_to_args( emitter_def["enemy"])
            self.create_emitter(
                pulse_emitter (
                    rate = 1.0 / 60.0,
                    start = emitter_def["t"],
                    x = emitter_def["location"][0],
                    y = emitter_def["location"][1],
                    ramp_speed = emitter_def["speed"],
                    driver = emitter_def["driver"],
                    template = factory_args,
                    factory = self
                    )
                )

    def render( self ):
        for enemy in self.enemies.tickables:
            enemies.primitive.render_shaded( enemies.shader, enemy.get_shader_params() )

