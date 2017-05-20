import beagle_runtime
from .src import game_instance as game

http_handler = game

def init():
    game.init()

def tick():
    game.tick()

def render():
    game.render()

def finalize():
    game.finalize()

def configure( application_ini ):
    game.configure( application_ini )

def http_serve_index():
    return "<H1>YO BUBZ</H1>"

def http_route_json(json):
    return json
